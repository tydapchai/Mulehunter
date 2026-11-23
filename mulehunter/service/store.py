import json
import sqlite3

from mulehunter.graph import LIMIT, WINDOW, Transfer


class SQLiteStore:
    def __init__(self, path):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS decisions (id TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS transfers (
                id TEXT PRIMARY KEY, source TEXT, target TEXT, amount REAL, currency TEXT, ts REAL
            );
            CREATE INDEX IF NOT EXISTS outgoing ON transfers(source, ts);
            CREATE INDEX IF NOT EXISTS incoming ON transfers(target, ts);
        """)

    def run(self, operation):
        with self.db:
            return operation(self)

    def get(self, identity):
        row = self.db.execute("SELECT body FROM decisions WHERE id = ?", (identity,)).fetchone()
        return json.loads(row[0]) if row else None

    def save(self, identity, record):
        self.db.execute("INSERT OR REPLACE INTO decisions VALUES (?, ?)",
                        (identity, json.dumps(record)))

    def add(self, event):
        self.db.execute("INSERT INTO transfers VALUES (?, ?, ?, ?, ?, ?)", (
            event.transaction_id, event.source_account, event.target_account,
            event.amount, event.currency, event.timestamp))

    def adjacent(self, node, timestamp):
        rows = self.db.execute("""
            SELECT * FROM transfers WHERE (source = ? OR target = ?) AND ts >= ? AND ts < ?
            ORDER BY ts DESC, id DESC LIMIT ?
        """, (node, node, timestamp - WINDOW, timestamp, LIMIT))
        return [Transfer(*row) for row in reversed(list(rows))]


class MemgraphStore:
    def __init__(self, uri):
        from neo4j import GraphDatabase
        self.driver = GraphDatabase.driver(uri, auth=None, connection_timeout=3)
        self.initialized = False

    def run(self, operation):
        with self.driver.session() as session:
            if not self.initialized:
                for label in ("Account", "Decision"):
                    session.run(f"CREATE INDEX ON :{label}(id)").consume()
                self.initialized = True
            with session.begin_transaction() as transaction:
                result = operation(MemgraphTransaction(transaction))
                transaction.commit()
                return result


class MemgraphTransaction:
    def __init__(self, tx):
        self.tx = tx

    def get(self, identity):
        row = self.tx.run("MATCH (d:Decision {id: $id}) RETURN d.body AS body", id=identity).single()
        return json.loads(row["body"]) if row else None

    def save(self, identity, record):
        self.tx.run("MERGE (d:Decision {id: $id}) SET d.body = $body",
                    id=identity, body=json.dumps(record)).consume()

    def add(self, event):
        self.tx.run("""
            MERGE (s:Account {id: $source})
            MERGE (t:Account {id: $target})
            CREATE (s)-[:TRANSFER {id: $id, amount: $amount, currency: $currency, ts: $ts, source: $source, target: $target}]->(t)
        """, source=event.source_account, target=event.target_account, id=event.transaction_id,
             amount=event.amount, currency=event.currency, ts=event.timestamp).consume()

    def adjacent(self, node, timestamp):
        return self.adjacent_many([node], timestamp)[node]

    def adjacent_many(self, nodes, timestamp):
        records = self.tx.run("""
            UNWIND $nodes AS node
            CALL {
                WITH node
                MATCH (a:Account {id: node})-[r:TRANSFER]-(:Account)
                WHERE r.ts >= $start AND r.ts < $end
                RETURN DISTINCT r.id AS id, r.source AS source, r.target AS target,
                                r.amount AS amount, r.currency AS currency, r.ts AS ts
                ORDER BY ts DESC, id DESC LIMIT $limit
            }
            RETURN node, id, source, target, amount, currency, ts
        """, nodes=nodes, start=timestamp - WINDOW, end=timestamp, limit=LIMIT)
        results = {node: [] for node in nodes}
        for row in records:
            node, *fields = row.values()
            results[node].append(Transfer(*fields))
        for edges in results.values():
            edges.sort(key=lambda edge: (edge.timestamp, edge.transaction_id))
        return results
