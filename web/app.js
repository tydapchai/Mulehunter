const statusLine = document.querySelector("#message");
const decisions = document.querySelector("#decisions");
const details = document.querySelector("#details");
const graph = cytoscape({
  container: document.querySelector("#graph"),
  style: [
    { selector: "node", style: {label: "data(label)", "background-color": "#29736a", color: "#162d29", "font-size": 11} },
    { selector: "edge", style: {"curve-style": "bezier", "target-arrow-shape": "triangle", "line-color": "#8da8a0", "target-arrow-color": "#8da8a0"} },
    { selector: ".candidate", style: {"line-style": "dashed", width: 4, "line-color": "#ac4329", "target-arrow-color": "#ac4329"} },
  ],
});

async function request(url, body) {
  const response = await fetch(url, body === undefined ? {} : {
    method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail));
  return data;
}

const decisionUrl = id => "/v1/decisions/" + encodeURIComponent(id);
const shortName = name => name.split(":").at(-1);

function show(record) {
  details.replaceChildren();
  const text = document.createElement("span");
  text.textContent = [
    record.status, record.event.amount.toLocaleString() + " " + record.event.currency,
    record.risk_score != null && "Score " + formatScore(record.risk_score),
    record.rule_hits.join(", ") || "No rule hits",
    record.model_version && "Model " + record.model_version,
    record.hold_until && "Until " + new Date(record.hold_until * 1000).toLocaleTimeString(),
  ].filter(Boolean).join(" · ");
  details.append(text);
  if (record.status === "PENDING_VERIFICATION") {
    for (const verified of [true, false]) {
      const button = document.createElement("button");
      button.textContent = verified ? "Simulate pass" : "Simulate failure";
      button.onclick = async () => {
        try {
          await request(decisionUrl(record.transaction_id) + "/verify", {verified});
          show(await request(decisionUrl(record.transaction_id)));
        } catch (error) { statusLine.textContent = error.message; }
      };
      details.append(button);
    }
  }
  graph.elements().remove();
  const elements = record.graph.nodes.map(node => ({data: {id: "node:" + node, label: shortName(node)}}));
  for (const [event, candidate] of [...record.graph.edges.map(edge => [edge, false]), [record.event, true]]) {
    elements.push({data: {id: "edge:" + event.transaction_id, source: "node:" + event.source_account,
      target: "node:" + event.target_account}, classes: candidate ? "candidate" : ""});
  }
  graph.add(elements);
  graph.layout({name: "breadthfirst", directed: false, padding: 25}).run();
}

function addRow(record) {
  const row = decisions.insertRow(0);
  const button = document.createElement("button");
  button.className = "link";
  button.textContent = shortName(record.event.source_account) + " → " + shortName(record.event.target_account);
  button.onclick = async () => {
    try { show(await request(decisionUrl(record.transaction_id))); }
    catch (error) { statusLine.textContent = error.message; }
  };
  row.insertCell().append(button);
  for (const value of [record.decision, record.path, record.risk_score?.toFixed(3) ?? "—", utcTime(record.event.timestamp)]) {
    row.insertCell().textContent = value;
  }
  if (decisions.rows.length > 100) decisions.deleteRow(-1);
  show(record);
}

function bind(selector, submit) {
  document.querySelector(selector).addEventListener("submit", async event => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector("button");
    button.disabled = true;
    statusLine.textContent = "Processing…";
    try { await submit(Object.fromEntries(new FormData(form))); statusLine.textContent = ""; }
    catch (error) { statusLine.textContent = error.message; }
    finally { button.disabled = false; }
  });
}

bind("#transfer", async form => {
  const id = crypto.randomUUID();
  await request("/v1/screen", {...form, amount: Number(form.amount), transaction_id: id, timestamp: new Date().toISOString()});
  addRow(await request(decisionUrl(id)));
});

bind("#replay", async form => {
  const {transactions} = await request("/v1/replay/" + form.pattern, {});
  for (const id of transactions) {
    for (let attempt = 0; attempt <= 40; attempt++) {
      const response = await fetch(decisionUrl(id));
      if (response.ok) { addRow(await response.json()); break; }
      if (response.status !== 404 || attempt === 40) throw new Error("Replay result unavailable for " + id);
      await new Promise(resolve => setTimeout(resolve, 250));
    }
  }
});
const streamUrl = "/v1/continuous-replay";
const streamSource = document.querySelector("#stream-source");
const streamStatus = document.querySelector("#stream-status");
const streamProgress = document.querySelector("#stream-progress");
const streamMode = document.querySelector("#stream-mode");
const startReplay = document.querySelector("#start-replay");
const pauseReplay = document.querySelector("#pause-replay");
const resetReplay = document.querySelector("#reset-replay");
const evaluation = document.querySelector("#evaluation");
const queue = document.querySelector("#alerts");
const queueFilter = document.querySelector("#queue-filter");
const queueStatus = document.querySelector("#queue-status");
const replayState = {
  metadata: null, cursor: 0, pending: [], findings: [], policyFindings: [],
  alerts: 0, rules: 0, running: false, generation: 0,
};

const utcTime = timestamp => new Date(timestamp * 1000).toISOString().slice(11, 19);
const formatScore = score => score == null ? "—" : score.toPrecision(3);

function updateReplayControls() {
  const {metadata, running, cursor} = replayState;
  startReplay.disabled = !metadata || running || cursor >= metadata.count;
  startReplay.textContent = cursor ? "Resume replay" : "Start replay";
  pauseReplay.disabled = !running || cursor >= metadata.count;
  resetReplay.disabled = !metadata || (!cursor && !running);
  streamMode.disabled = running || cursor > 0;
  streamProgress.value = cursor;
}

function replayRow(record, mode, parent, isFinding) {
  const {event, rule_hits: rules} = record;
  const decision = record[mode + "_decision"];
  const score = record[mode + "_score"];
  const row = parent.insertRow(isFinding ? -1 : 0);
  const transfer = document.createElement("button");
  transfer.className = "link";
  transfer.textContent = shortName(event.source_account) + " → " + shortName(event.target_account);
  transfer.onclick = async () => {
    try {
      const evidence = rules.length || record.all_decision !== "ALLOW";
      const graph = evidence ? await request(streamUrl + "/graphs/" + encodeURIComponent(event.transaction_id)) :
        {nodes: [...new Set([event.source_account, event.target_account])], edges: []};
      show({event, graph, rule_hits: rules, status: decision, risk_score: score,
        model_version: score == null ? null : replayState.metadata.model_version});
    } catch (error) { streamStatus.textContent = error.message; }
  };
  if (isFinding) row.insertCell().textContent = utcTime(event.timestamp);
  row.insertCell().append(transfer);
  const values = isFinding ? [decision, rules.join(", ") || "Model score", formatScore(score)] :
    [decision, score == null ? "fast" : "deep", formatScore(score), utcTime(event.timestamp)];
  for (const value of values) row.insertCell().textContent = value;
  row.classList.add("historical");
}

function renderQueue() {
  const {policyFindings, findings, alerts, rules} = replayState;
  const records = queueFilter.value === "alerts" ? policyFindings : findings;
  queue.replaceChildren();
  for (const record of records.slice(0, 30)) replayRow(record, streamMode.value, queue, true);
  queueStatus.textContent = replayState.cursor ?
    alerts + " policy alerts · " + rules + " transfers with rule hits" :
    "Start replay to see policy alerts and rule hits.";
}

function renderEvaluation(report) {
  const table = document.createElement("table");
  const headings = ["Mode", "Scored", "True alerts", "Positive skipped", "Positive below threshold", "False alerts / 1,000"];
  const head = table.createTHead().insertRow();
  for (const name of headings) {
    const cell = document.createElement("th");
    cell.textContent = name;
    head.append(cell);
  }
  const body = table.createTBody();
  for (const [key, label] of [["gated", "Fast Path → GraphSAGE"], ["all", "GraphSAGE only"]]) {
    const result = report.modes[key];
    const row = body.insertRow();
    for (const value of [label, result.scored, result.true_alerts, result.positive_skipped,
      result.positive_scored_below_threshold, result.false_alerts_per_1000.toFixed(2)]) {
      row.insertCell().textContent = value;
    }
  }
  document.querySelector("#evaluation-results").replaceChildren(table);
  evaluation.hidden = false;
}

function resetStream() {
  Object.assign(replayState, {cursor: 0, pending: [], findings: [], policyFindings: [],
    alerts: 0, rules: 0, running: false, generation: replayState.generation + 1});
  decisions.querySelectorAll(".historical").forEach(row => row.remove());
  graph.elements().remove();
  details.replaceChildren();
  evaluation.hidden = true;
  streamStatus.textContent = "Ready to replay";
  renderQueue();
  updateReplayControls();
}

async function playStream() {
  const state = replayState;
  const generation = ++state.generation;
  const mode = streamMode.value;
  state.running = true;
  updateReplayControls();
  try {
    while (state.running && state.generation === generation && state.cursor < state.metadata.count) {
      if (!state.pending.length) {
        const page = await request(streamUrl + "/events?offset=" + state.cursor);
        if (state.generation !== generation || !state.running) return;
        if (!page.length) throw new Error("Replay data ended before the expected count.");
        state.pending = page;
      }
      const speed = Number(document.querySelector("#stream-speed").value);
      const batch = state.pending.splice(0, Math.max(1, Math.floor(speed / 5)));
      let queueChanged = false;
      for (const record of batch) {
        const alert = record[mode + "_decision"] !== "ALLOW";
        if (alert) {
          state.alerts++;
          state.policyFindings.unshift(record);
          state.policyFindings.length = Math.min(30, state.policyFindings.length);
        }
        if (record.rule_hits.length) state.rules++;
        if (alert || record.rule_hits.length) {
          state.findings.unshift(record);
          state.findings.length = Math.min(30, state.findings.length);
          queueChanged = true;
        }
      }
      for (const record of batch.slice(-30)) replayRow(record, mode, decisions, false);
      while (decisions.rows.length > 50) decisions.deleteRow(-1);
      state.cursor += batch.length;
      if (queueChanged) renderQueue();
      streamStatus.textContent = state.cursor.toLocaleString() + " / " +
        state.metadata.count.toLocaleString() + " screened · " + utcTime(batch.at(-1).event.timestamp) + " UTC";
      updateReplayControls();
      if (state.cursor < state.metadata.count) await new Promise(resolve => setTimeout(resolve, 200));
    }
    if (state.generation === generation && state.cursor === state.metadata.count) {
      const report = await request(streamUrl + "/report");
      if (state.generation === generation) renderEvaluation(report);
    }
  } catch (error) {
    if (state.generation === generation) streamStatus.textContent = error.message;
  } finally {
    if (state.generation === generation) {
      state.running = false;
      updateReplayControls();
    }
  }
}

startReplay.onclick = playStream;
pauseReplay.onclick = () => {
  replayState.running = false;
  replayState.generation++;
  streamStatus.textContent = "Paused at " + replayState.cursor.toLocaleString() + " transfers";
  updateReplayControls();
};
resetReplay.onclick = resetStream;
queueFilter.onchange = renderQueue;
request(streamUrl + "/metadata").then(metadata => {
  replayState.metadata = metadata;
  streamProgress.max = metadata.count;
  streamSource.textContent = metadata.source + " · " + metadata.start.slice(0, 16).replace("T", " ") +
    " UTC · " + metadata.count.toLocaleString() + " transfers · model " + metadata.model_version;
  resetStream();
}).catch(error => { streamSource.textContent = error.message; });
