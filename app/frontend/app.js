const API="/api/v1";
const $=id=>document.getElementById(id);
const state={failures:[],summary:null,experiment:null,experiments:[]};
async function api(path,options){options=options||{};const r=await fetch(API+path,{headers:{"Content-Type":"application/json"},...options});const d=await r.json().catch(()=>({}));if(!r.ok)throw new Error((d.error&&d.error.message)||d.detail||"Request failed ("+r.status+")");return d;}
function esc(v){return String(v==null?"":v).replace(/[&<>"\']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","\'":"&#039;"}[c]));}
function toast(m){const e=$("toast");e.textContent=m;e.classList.add("show");setTimeout(()=>e.classList.remove("show"),2500)}
function view(v){document.querySelectorAll(".view").forEach(e=>e.classList.toggle("active",e.id==="view-"+v));document.querySelectorAll(".nav-button").forEach(e=>e.classList.toggle("active",e.dataset.view===v));if(v==="overview")loadOverview();if(v==="experiments")loadExperiments();if(v==="failures")loadFailures()}
document.querySelectorAll(".nav-button").forEach(b=>b.onclick=()=>view(b.dataset.view));
async function loadOverview(){try{const m=await api("/metrics");$("runsTotal").textContent=m.runs_total;$("runsCompleted").textContent=m.runs_completed;$("failuresTotal").textContent=m.failures_total;$("avgLatency").textContent=m.average_latency_ms==null?"—":m.average_latency_ms+" ms";$("metricsDetail").innerHTML=[["Failed runs",m.runs_failed],["Input tokens",m.input_tokens_total],["Output tokens",m.output_tokens_total],["Cost",m.cost_total]].map(x=>"<dt>"+esc(x[0])+"</dt><dd>"+esc(x[1])+"</dd>").join("")}catch(e){toast(e.message)}loadReadiness()}
async function loadReadiness(){try{const r=await fetch("/health/readiness"),d=await r.json();$("systemStatus").textContent=d.status==="ready"?"System ready":"System not ready";$("systemStatus").className="status "+(d.status==="ready"?"ready":"warning");$("readinessDetail").innerHTML=Object.entries(d.checks||{}).map(x=>"<dt>"+esc(x[0])+"</dt><dd>"+(x[1]?"Ready":"Not ready")+"</dd>").join("")}catch(e){$("systemStatus").textContent="System unavailable";$("systemStatus").className="status warning"}}
$("qaForm").onsubmit=async e=>{e.preventDefault();const t=$("qaResult");t.className="result-grid";t.innerHTML="<section class=panel>Running…</section>";try{const d=await api("/qa",{method:"POST",body:JSON.stringify({question:$("qaQuestion").value,top_k:+$("qaTopK").value})});t.innerHTML="<section class=panel><p class=eyebrow>Answer</p><h2>Generated response</h2><p class=answer>"+esc(d.answer)+"</p><div class=uncertainty><strong>Uncertainty:</strong> "+esc(d.uncertainty||"Not reported")+"</div></section><section class=panel><p class=eyebrow>Traceability</p><h2>Evidence</h2><div class=evidence-list>"+d.evidence.map(x=>"<article class=evidence><strong>"+esc(x.chunk_id)+"</strong><span> · "+esc(x.document_id)+"</span><p>"+esc(x.text)+"</p></article>").join("")+"</div></section>"}catch(e){t.innerHTML="<section class=panel error>"+esc(e.message)+"</section>"}};
$("experimentForm").onsubmit=async e=>{e.preventDefault();try{const d=await api("/experiments",{method:"POST",body:JSON.stringify({name:$("experimentName").value,description:$("experimentDescription").value,model_config:{provider:"ollama"},embedding_config:{provider:"local-baseline"},retriever_config:{type:"baseline"},top_k:+$("experimentTopK").value,prompt_version:$("experimentPrompt").value,benchmark_version:$("experimentBenchmark").value})});selectExperiment(d);await loadExperiments();toast("Experiment created")}catch(e){toast(e.message)}};
$("runForm").onsubmit=async e=>{e.preventDefault();if(!state.experiment){toast("Create an experiment first");return}const t=$("runResult");t.className="result-card";t.textContent="Running question…";try{const d=await api("/experiments/"+encodeURIComponent(state.experiment.experiment_id)+"/runs",{method:"POST",body:JSON.stringify({question_id:$("runQuestionId").value,question:$("runQuestion").value,domain:"depression",difficulty:$("runDifficulty").value,expected_evidence:$("runEvidence").value.split(",").map(x=>x.trim()).filter(Boolean),reference_answer:$("runReference").value,key_concepts:$("runConcepts").value.split(",").map(x=>x.trim()).filter(Boolean)})});t.innerHTML="<strong>"+esc(d.status)+"</strong><span>Run "+esc(d.run_id)+"</span><span>Latency: "+esc(d.latency_ms)+" ms</span><span>Tokens: "+((d.input_tokens||0)+(d.output_tokens||0))+"</span>";loadOverview()}catch(e){t.innerHTML="<span class=error-text>"+esc(e.message)+"</span>"}};
$("comparisonForm").onsubmit=async e=>{e.preventDefault();const t=$("comparisonResult");t.textContent="Comparing…";try{const d=await api("/comparisons",{method:"POST",body:JSON.stringify({baseline_experiment_id:$("baselineId").value,candidate_experiment_id:$("candidateId").value})});t.innerHTML="<p class=muted>Benchmark: "+esc(d.benchmark_version)+"</p><div class=metric-table><table><thead><tr><th>Metric</th><th>Baseline</th><th>Candidate</th><th>Delta</th></tr></thead><tbody>"+d.metric_deltas.map(x=>"<tr><td>"+esc(x.metric)+"</td><td>"+x.baseline.toFixed(3)+"</td><td>"+x.candidate.toFixed(3)+"</td><td>"+(x.delta>=0?"+":"")+x.delta.toFixed(3)+"</td></tr>").join("")+"</tbody></table></div>"}catch(e){t.innerHTML="<span class=error-text>"+esc(e.message)+"</span>"}};
async function loadFailures(){try{const a=await api("/failures"),s=await api("/failures/summary");state.failures=a.failures;state.summary=s;renderFailures()}catch(e){toast(e.message)}}
function renderFailures(){const s=state.summary||{total:0,by_category:{},by_severity:{}};$("failureTotal").textContent=s.total;$("failureCritical").textContent=s.by_severity.CRITICAL||0;$("failureHigh").textContent=s.by_severity.HIGH||0;$("failureCategories").textContent=Object.keys(s.by_category).length;const sel=$("categoryFilter"),old=sel.value;sel.replaceChildren(new Option("All categories",""));Object.keys(s.by_category).sort().forEach(c=>sel.add(new Option(c,c)));sel.value=old;const c=sel.value,z=$("severityFilter").value;$("failureRows").replaceChildren(...state.failures.filter(f=>(!c||f.category===c)&&(!z||f.severity===z)).map(f=>{const r=document.createElement("tr");r.innerHTML="<td><strong>"+esc(f.failure_id)+"</strong></td><td>"+esc(f.category)+"</td><td>"+esc(f.type)+"</td><td><span class=badge>"+esc(f.severity)+"</span></td><td>"+esc(f.question_id)+"</td>";r.onclick=()=>detail(f);return r}));const entries=Object.entries(s.by_category),max=Math.max(...entries.map(x=>x[1]),1);$("categoryBars").innerHTML=entries.map(x=>"<div class=bar-row><span>"+esc(x[0])+"</span><div class=bar><i style=\"width:"+(x[1]/max*100)+"%\"></i></div><strong>"+x[1]+"</strong></div>").join("")}
function detail(f){$("failureDetail").classList.remove("empty");$("failureDetail").innerHTML="<dl class=detail-list>"+[["Failure ID",f.failure_id],["Category",f.category],["Type",f.type],["Severity",f.severity],["Run",f.run_id],["Question",f.question_id],["Metric",(f.metric||"—")+" "+(f.metric_value==null?"":"= "+f.metric_value)],["Description",f.description],["Evidence",f.evidence],["Classifier",f.classifier_version]].map(x=>"<dt>"+esc(x[0])+"</dt><dd>"+esc(x[1])+"</dd>").join("")+"</dl><div class=trace>Question → Run → Answer/Evaluation → Failure → Metric signal → Evidence</div><button type=button class=primary id=inspectFailureEvidence>Inspect this run in Evidence Explorer</button>";$("inspectFailureEvidence").onclick=()=>{view("failures");$("evidenceExplorerRunId").value=f.run_id;loadEvidenceExplorer();window.scrollTo({top:0,behavior:"smooth"})}}
async function loadFailureAnalysis(){
  const experimentId=$("failureExperimentId").value.trim();
  const dimension=$("failureDimension").value;
  if(!experimentId){toast("Enter an experiment ID");return}
  try{
    const [analysis,rates]=await Promise.all([
      api("/failures/experiments/"+encodeURIComponent(experimentId)+"/analysis"),
      api("/failures/experiments/"+encodeURIComponent(experimentId)+"/rates?dimension="+encodeURIComponent(dimension))
    ]);
    $("failureAnalysis").classList.remove("empty");
    $("failureAnalysis").innerHTML="<dl class=detail-list><dt>Experiment</dt><dd>"+esc(analysis.experiment_id)+"</dd><dt>Completed questions</dt><dd>"+esc(analysis.completed_questions)+"</dd><dt>Total failures</dt><dd>"+esc(analysis.total_failures)+"</dd><dt>Affected questions</dt><dd>"+esc(analysis.unique_questions)+"</dd></dl>";
    $("failureRateRows").replaceChildren(...rates.rates.map(x=>{
      const r=document.createElement("tr");
      r.innerHTML="<td>"+esc(x.dimension)+"</td><td>"+esc(x.value)+"</td><td>"+esc(x.failure_count)+"</td><td>"+esc(x.unique_questions)+"</td><td>"+(x.failure_rate*100).toFixed(1)+"%</td>";
      return r;
    }));
  }catch(e){$("failureAnalysis").textContent=e.message;$("failureAnalysis").className="detail error"}
}
async function loadFailureRegression(){
  const baseline=$("failureBaselineId").value.trim();
  const candidate=$("failureCandidateId").value.trim();
  const threshold=+$("failureRegressionThreshold").value;
  const target=$("failureRegressionResult");
  if(!baseline||!candidate){toast("Enter both experiment IDs");return}
  target.className="detail";
  target.textContent="Comparing…";
  try{
    const d=await api("/failures/regression?baseline_experiment_id="+encodeURIComponent(baseline)+"&candidate_experiment_id="+encodeURIComponent(candidate)+"&threshold="+encodeURIComponent(threshold));
    const flagged=d.regressions.filter(x=>x.regression||x.question_level_regression);
    target.innerHTML="<p>Threshold: "+(d.threshold*100).toFixed(1)+" percentage points</p><div class=metric-table><table><thead><tr><th>Category</th><th>Type</th><th>Baseline</th><th>Candidate</th><th>Delta</th><th>Signal</th></tr></thead><tbody>"+d.regressions.map(x=>"<tr><td>"+esc(x.category)+"</td><td>"+esc(x.failure_type)+"</td><td>"+(x.baseline_rate*100).toFixed(1)+"%</td><td>"+(x.candidate_rate*100).toFixed(1)+"%</td><td>"+(x.rate_difference*100).toFixed(1)+"pp</td><td>"+(x.regression?"Rate regression":"")+(x.question_level_regression?" Question-level regression":"")+"</td></tr>").join("")+"</tbody></table></div><p>"+flagged.length+" regression signal(s).</p>";
  }catch(e){target.textContent=e.message}
}
async function loadEvidenceExplorer(){
  const runId=$("evidenceExplorerRunId").value.trim();
  const target=$("evidenceExplorerResult");
  if(!runId){toast("Enter a run ID");return}
  target.className="detail";
  target.textContent="Loading evidence trace…";
  try{
    const d=await api("/runs/"+encodeURIComponent(runId)+"/evidence/explorer");
    const claims=d.claims||[];
    const chunks=d.chunks||[];
    const docs=d.documents||[];
    target.innerHTML=
      "<div class=trace><strong>Question</strong><p>"+esc(d.question||d.question_id)+"</p><strong>Answer</strong><p>"+esc(d.answer||"—")+"</p>"+
      (d.uncertainty?"<strong>Uncertainty</strong><p>"+esc(d.uncertainty)+"</p>":"")+
      "</div>"+
      "<h3>Claims and citations</h3>"+
      "<div class=trace-list>"+claims.map(c=>"<article class=detail-card><strong>Claim "+c.claim_index+"</strong><p>"+esc(c.text)+"</p><span>"+(c.citations.length?c.citations.map(x=>"Citation → "+esc(x.chunk_id)).join(" · "):"No citation")+"</span></article>").join("")+"</div>"+
      "<h3>Retrieved evidence</h3>"+
      "<div class=table-wrap><table><thead><tr><th>Rank</th><th>Chunk</th><th>Document</th><th>Score</th><th>Use</th></tr></thead><tbody>"+
      chunks.map(c=>"<tr><td>"+c.rank+"</td><td>"+esc(c.chunk_id)+"</td><td>"+esc(c.document_id)+"</td><td>"+(c.score==null?"—":Number(c.score).toFixed(4))+"</td><td>"+(c.used_in_citation?"Cited":"Retrieved only")+"</td></tr>").join("")+
      "</tbody></table></div>"+
      "<h3>Documents</h3><div class=trace-list>"+docs.map(x=>"<article class=detail-card><strong>"+esc(x.title)+"</strong><p>"+esc(x.organization)+" · "+esc(x.source)+"</p><span>"+esc(x.document_id)+"</span></article>").join("")+"</div>";
  }catch(e){target.className="detail error";target.textContent=e.message}
}
$("evidenceExplorerForm").onsubmit=e=>{e.preventDefault();loadEvidenceExplorer()};
$("failureAnalyze").onclick=loadFailureAnalysis;
$("failureRegressionForm").onsubmit=e=>{e.preventDefault();loadFailureRegression()};
$("categoryFilter").onchange=renderFailures;$("severityFilter").onchange=renderFailures;loadOverview();
async function loadExperiments(){try{const d=await api("/experiments");state.experiments=d.experiments||[];renderExperiments();if(state.experiment){const fresh=state.experiments.find(x=>x.experiment_id===state.experiment.experiment_id);if(fresh)selectExperiment(fresh)}}catch(e){toast(e.message)}}
function renderExperiments(){const target=$("experimentList");if(!state.experiments.length){target.innerHTML="<div class=empty>No experiments found.</div>";return}target.innerHTML=state.experiments.map(x=>"<button type=button class=\"experiment-item\" data-id=\""+esc(x.experiment_id)+"\"><strong>"+esc(x.name)+"</strong><span>"+esc(x.benchmark_version)+" · "+esc(x.prompt_version)+"</span><small>"+esc(x.experiment_id)+"</small></button>").join("");target.querySelectorAll(".experiment-item").forEach(b=>b.onclick=()=>{const item=state.experiments.find(x=>x.experiment_id===b.dataset.id);if(item)selectExperiment(item)})}
function selectExperiment(d){state.experiment=d;$("experimentTitle").textContent=d.name;$("experimentState").innerHTML="<dl class=detail-list><dt>ID</dt><dd>"+esc(d.experiment_id)+"</dd><dt>Benchmark</dt><dd>"+esc(d.benchmark_version)+"</dd><dt>Prompt</dt><dd>"+esc(d.prompt_version)+"</dd><dt>Top K</dt><dd>"+d.top_k+"</dd></dl>";$("baselineId").value=d.experiment_id;loadExperimentReport(d.experiment_id);document.querySelectorAll(".experiment-item").forEach(b=>b.classList.toggle("selected",b.dataset.id===d.experiment_id))}
async function loadExperimentReport(id){const target=$("experimentReport");target.className="detail";target.textContent="Loading metrics…";try{const d=await api("/experiments/"+encodeURIComponent(id)+"/report");const r=d.configuration.reproducibility||{};const metrics=Object.entries(d.metrics||{});target.innerHTML="<div class=panel-head><div><p class=eyebrow>Research artifact</p><h2>Reproducible report</h2></div><a class=primary href=\""+API+"/experiments/"+encodeURIComponent(id)+"/report/markdown\" target=\"_blank\" rel=\"noopener\">Open Markdown report</a></div><dl class=detail-list><dt>Completed runs</dt><dd>"+esc(d.sample_count)+"</dd><dt>Config hash</dt><dd><code>"+esc(r.config_hash||"—")+"</code></dd><dt>Model</dt><dd>"+esc(r.model_version||"—")+"</dd><dt>Embedding</dt><dd>"+esc(r.embedding_version||"—")+"</dd><dt>Retriever</dt><dd>"+esc(r.retriever_version||"—")+"</dd><dt>Runtime</dt><dd>"+esc(r.runtime_version||"—")+"</dd></dl><h3>Metrics</h3><div class=metric-table><table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>"+(metrics.length?metrics.map(x=>"<tr><td>"+esc(x[0])+"</td><td>"+Number(x[1]).toFixed(3)+"</td></tr>").join(""):"<tr><td colspan=2>No completed evaluation metrics.</td></tr>")+"</tbody></table></div>"}catch(e){target.className="detail error";target.textContent=e.message}}
$("refreshExperiments").onclick=loadExperiments;
