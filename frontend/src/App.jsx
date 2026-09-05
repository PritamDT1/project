import { useEffect, useState } from 'react'
import { Bot, BrainCircuit, ChevronRight, CircleUserRound, FileText, FlaskConical, History as HistoryIcon, LoaderCircle, LogOut, Moon, Orbit, Send, ShieldCheck, Sparkles, UploadCloud } from 'lucide-react'

const configuredApiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_URL = configuredApiUrl.startsWith('http') ? configuredApiUrl : `https://${configuredApiUrl}`
const supportedTypes = ['PDF', 'DOCX', 'TXT', 'MD', 'PPTX', 'CSV', 'XLSX', 'JSON']
const geminiModels = ['google_genai:gemini-3.6-flash', 'google_genai:gemini-3.5-flash', 'google_genai:gemini-3.5-flash-lite']

function LoadingScreen() {
  return <div className="loading-screen"><div className="loading-orbit"><Orbit size={38} /><span /></div><p className="eyebrow">Research Orbit</p><h1>Initializing workspace</h1><div className="loading-bar"><i /></div></div>
}

function Auth({ onAuth }) {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ aadhaar: '', email: '', name: '', age: '', phone: '' })
  const [error, setError] = useState('')
  const update = (key) => (event) => setForm({ ...form, [key]: event.target.value })
  const submit = async (event) => {
    event.preventDefault()
    if (!form.aadhaar || !form.email || (mode === 'register' && (!form.name || !form.age || !form.phone))) return setError('Complete all required fields to continue.')
    if (!form.email.includes('@')) return setError('Enter a valid email address.')
    try {
      const response = await fetch(`${API_URL}/auth/${mode}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      if (!response.ok) throw new Error((await response.json()).detail || 'Authentication failed.')
      onAuth(await response.json())
    } catch (requestError) {
      setError(requestError.message.includes('Failed to fetch') ? 'API unavailable. Start the Python backend or check VITE_API_URL.' : requestError.message)
    }
  }
  return <main className="auth-page"><section className="auth-card"><div className="brand"><span className="brand-icon"><Orbit size={20} /></span><span><b>Research Orbit</b><small>Private intelligence workspace</small></span></div><p className="eyebrow">Secure access</p><h1>Welcome back</h1><p className="muted">Sign in to your documents, model workspace, and conversation history.</p><div className="auth-tabs"><button className={mode === 'login' ? 'active' : ''} onClick={() => { setMode('login'); setError('') }}>Log in</button><button className={mode === 'register' ? 'active' : ''} onClick={() => { setMode('register'); setError('') }}>Create account</button></div>{error && <div className="error"><ShieldCheck size={15} />{error}</div>}<form onSubmit={submit}><Field label="Aadhaar card number"><input inputMode="numeric" value={form.aadhaar} onChange={update('aadhaar')} /></Field>{mode === 'register' && <div className="two-col"><Field label="Name"><input value={form.name} onChange={update('name')} /></Field><Field label="Age"><input type="number" min="1" max="120" value={form.age} onChange={update('age')} /></Field></div>}<Field label="Email"><input type="email" value={form.email} onChange={update('email')} /></Field>{mode === 'register' && <Field label="Phone number"><input value={form.phone} onChange={update('phone')} /></Field>}<button className="primary wide" type="submit">{mode === 'login' ? 'Enter workspace' : 'Create account'}<ChevronRight size={16} /></button></form></section></main>
}

function Field({ label, children }) { return <label className="field"><span>{label}</span>{children}</label> }

function Shell({ user, onLogout }) {
  const [page, setPage] = useState('assistant')
  return <div className="app-shell"><aside className="sidebar"><div className="brand"><span className="brand-icon"><Orbit size={20} /></span><span><b>Research Orbit</b><small>Private workspace</small></span></div><p className="nav-title">Workspace</p><nav><button className={page === 'assistant' ? 'nav-active' : ''} onClick={() => setPage('assistant')}><FileText size={17} />Document assistant</button><button className={page === 'maker' ? 'nav-active' : ''} onClick={() => setPage('maker')}><FlaskConical size={17} />Models</button><button className={page === 'history' ? 'nav-active' : ''} onClick={() => setPage('history')}><HistoryIcon size={17} />History</button></nav><div className="sidebar-bottom"><div className="user"><CircleUserRound size={18} /><span>{user?.name || user?.email || 'Signed in'}<small>Active session</small></span></div><button className="logout" onClick={onLogout}><LogOut size={15} />Log out</button></div></aside><main className="workspace"><header className="topbar"><span className="eyebrow">{page === 'maker' ? 'Model lab / supervised learning' : page === 'history' ? 'Workspace / conversation history' : 'Research orbit / RAG discovery'}</span><span className="status"><i />System ready <Moon size={14} /></span></header>{page === 'assistant' ? <Assistant user={user} /> : page === 'maker' ? <ModelMaker /> : <History user={user} />}</main></div>
}

function Hero({ title, copy, icon: Icon }) { return <section className="hero"><div className="hero-icon"><Icon size={22} /></div><div><p className="eyebrow">Private workspace</p><h1>{title}</h1><p className="hero-copy">{copy}</p></div></section> }

function Assistant({ user }) {
  const [tab, setTab] = useState('summarize')
  const [files, setFiles] = useState([])
  const [query, setQuery] = useState('Summarize the key points of this document.')
  const [modelName, setModelName] = useState(geminiModels[0])
  const [message, setMessage] = useState('')
  const run = async () => { if (tab !== 'ask' && !files.length) return setMessage('Upload at least one file to begin.'); if (!query.trim()) return setMessage('Enter a question or research prompt.'); setMessage('Analyzing documents...'); const body = new FormData(); files.forEach(file => body.append('files', file)); body.append('query', query); body.append('mode', tab); body.append('model_name', modelName); if (user?.aadhaar) body.append('aadhaar', user.aadhaar); try { const response = await fetch(`${API_URL}/documents/analyze`, { method: 'POST', body }); const data = await response.json(); if (!response.ok) throw new Error(data.detail || 'Analysis failed.'); setMessage(data.answer) } catch (error) { setMessage(error.message) } }
  return <><Hero icon={Bot} title="Researcher" copy="Summarize, compare, and interrogate your files across a focused, private knowledge workspace." /><div className="tabs">{[['summarize', 'Summarize'], ['compare', 'Compare'], ['ask', 'Ask questions']].map(([key, label]) => <button className={tab === key ? 'active' : ''} onClick={() => { setTab(key); setMessage('') }} key={key}>{label}</button>)}</div><section className="content-grid"><div className="panel"><div className="panel-head"><div><h2>{tab === 'compare' ? 'Compare files' : tab === 'ask' ? 'Ask anything' : 'Summarize files'}</h2><p>{tab === 'ask' ? 'Ask a general question or optionally add files for grounded answers.' : 'Upload sources and direct the research pass.'}</p></div><Sparkles size={19} /></div><label className="dropzone"><input type="file" multiple onChange={(event) => setFiles([...event.target.files])} /><UploadCloud size={26} /><strong>{files.length ? `${files.length} file(s) selected` : tab === 'ask' ? 'Optional files for context' : 'Drop files here or browse'}</strong><small>PDF, DOCX, TXT, CSV and more</small><span className="button">Choose files</span></label><div className="chips">{supportedTypes.map((type) => <span key={type}>{type}</span>)}</div><Field label="Gemini model"><select value={modelName} onChange={(event) => setModelName(event.target.value)}>{geminiModels.map((model) => <option value={model} key={model}>{model.replace('google_genai:', '')}</option>)}</select></Field><Field label={tab === 'ask' ? 'Question' : 'Research prompt'}><input value={query} onChange={(event) => setQuery(event.target.value)} /></Field><button className="primary" onClick={run}><Send size={15} />{tab === 'ask' ? 'Ask question' : 'Run research pass'}</button>{message && <div className="notice"><Answer content={message} /></div>}</div><aside className="panel metrics"><Metric label="Documents indexed" value={files.length} /><Metric label="Retrieval mode" value={files.length ? 'Gemini context' : 'General chat'} /><Metric label="Selected model" value={modelName.replace('google_genai:', '')} /><div className="metric-note">Files are optional for questions.</div></aside></section></>
}
function Metric({ label, value }) { return <div className="metric"><span>{label}</span><b>{value}</b></div> }

function Answer({ content }) {
  if (typeof content === 'string') return <div className="answer-content">{content}</div>
  if (!Array.isArray(content)) return null
  return <div className="answer-content">{content.map((block, index) => {
    if (block.type === 'text') return <div className="answer-block" key={index}>{block.text}</div>
    const imageUrl = block.url || block.image_url?.url || (block.data && `data:${block.mime_type || 'image/png'};base64,${block.data}`)
    return imageUrl ? <img key={index} src={imageUrl} alt="Model response" style={{ maxWidth: '100%', borderRadius: 8, marginTop: 12 }} /> : null
  })}</div>
}

function History({ user }) {
  const [entries, setEntries] = useState([])
  const [status, setStatus] = useState('Loading history...')
  useEffect(() => {
    fetch(`${API_URL}/history/${encodeURIComponent(user.aadhaar)}`)
      .then(async (response) => {
        const data = await response.json()
        if (!response.ok) throw new Error(data.detail || 'Could not load history.')
        setEntries(data)
        setStatus(data.length ? '' : 'No saved conversations yet.')
      })
      .catch((error) => setStatus(error.message))
  }, [user.aadhaar])
  return <><Hero icon={HistoryIcon} title="Conversation history" copy="Review your saved questions and responses from previous research sessions." /><section className="panel">{status && <div className="notice">{status}</div>}{entries.map((entry, index) => <article className="history-entry" key={`${entry.time}-${index}`}><div className="panel-head"><div><h2>{entry.question}</h2><p>{entry.time ? new Date(entry.time).toLocaleString() : 'Previous session'}</p></div></div><div className="history-response">{entry.response}</div></article>)}</section></>
}

function LegacyModelMaker() {
  const [trained, setTrained] = useState(false)
  const [prediction, setPrediction] = useState('')
  const predict = () => setPrediction(Math.random() > .5 ? 'Fraud' : 'Not Fraud')
  return <><Hero icon={BrainCircuit} title="Model Maker" copy="Turn a clean CSV into a tested prediction model with transparent feature selection and a live input check." /><div className="content-grid"><section className="panel"><div className="panel-head"><div><h2>Training configuration</h2><p>Configure the supervised learning pass.</p></div><span className="eyebrow">Scikit-learn</span></div><label className="dropzone compact"><input type="file" accept=".csv" onChange={() => setTrained(false)} /><UploadCloud size={23} /><strong>Upload a CSV dataset</strong><span className="button">Choose CSV</span></label><Field label="Target variable"><select defaultValue="fraud_status"><option>fraud_status</option><option>risk_level</option><option>approved</option></select></Field><Field label="Learning method"><select defaultValue="Random Forest Classifier"><option>Random Forest Classifier</option><option>Logistic Regression</option><option>Decision Tree Classifier</option></select></Field><button className="primary" onClick={() => setTrained(true)}><BrainCircuit size={15} />Train model</button>{trained && <div className="notice">Model trained. Validation set is ready.</div>}</section><section className="panel"><div className="panel-head"><div><h2>Feature selection</h2><p>Choose signals for the model.</p></div></div>{['transaction_amount', 'merchant_type', 'account_age_days', 'device_score', 'country_code'].map((feature, index) => <label className="feature" key={feature}><span>{feature}</span><input type="checkbox" defaultChecked={index < 3} /></label>)}<Metric label="Target classes" value="Not Fraud / Fraud" /><Metric label="Validation split" value="80 / 20" /></section></div><section className="panel check-panel"><div className="panel-head"><div><h2>Check model</h2><p>Enter values and inspect a classification result.</p></div><span className="eyebrow">Live input</span></div><div className="two-col"><Field label="Transaction amount"><input type="number" defaultValue="50" /></Field><Field label="Device score"><input type="number" defaultValue="50" /></Field></div><button className="primary" onClick={predict}><Send size={15} />Predict class</button>{prediction && <div className="result"><span>Predicted class</span><strong>{prediction}</strong><small>Uses the target labels, not numeric encoding.</small></div>}</section></>
}

function parseCsv(text) {
  const rows = []
  let row = [], value = '', quoted = false
  for (let index = 0; index < text.length; index += 1) {
    const character = text[index]
    if (character === '"') {
      if (quoted && text[index + 1] === '"') { value += '"'; index += 1 } else quoted = !quoted
    } else if (character === ',' && !quoted) { row.push(value.trim()); value = '' }
    else if ((character === '\n' || character === '\r') && !quoted) {
      if (character === '\r' && text[index + 1] === '\n') index += 1
      row.push(value.trim()); value = ''
      if (row.some(Boolean)) rows.push(row)
      row = []
    } else value += character
  }
  if (value || row.length) { row.push(value.trim()); rows.push(row) }
  const columns = (rows.shift() || []).map((column) => column.replace(/^\uFEFF/, ''))
  return { columns, rows: rows.filter((row) => row.some(Boolean)).slice(0, 50) }
}

function ModelMaker() {
  const [dataset, setDataset] = useState(null)
  const [columns, setColumns] = useState([])
  const [previewRows, setPreviewRows] = useState([])
  const [target, setTarget] = useState('')
  const [selectedFeatures, setSelectedFeatures] = useState([])
  const [method, setMethod] = useState('Random Forest Classifier')
  const [modelId, setModelId] = useState('')
  const [features, setFeatures] = useState([])
  const [featureTypes, setFeatureTypes] = useState({ numeric: [], categorical: [] })
  const [targetValues, setTargetValues] = useState([])
  const [status, setStatus] = useState('')
  const [prediction, setPrediction] = useState('')
  const [values, setValues] = useState({})
  const updateValue = (key) => (event) => setValues({ ...values, [key]: event.target.value })
  const train = async () => {
    if (!dataset) return setStatus('Upload a CSV dataset before training.')
    if (!target) return setStatus('Select the target variable from your CSV.')
    if (!selectedFeatures.length) return setStatus('Select at least one feature column.')
    setStatus('Training model...')
    const body = new FormData()
    body.append('file', dataset); body.append('target', target); body.append('method', method)
    body.append('features', JSON.stringify(selectedFeatures))
    try {
      const response = await fetch(`${API_URL}/models/train`, { method: 'POST', body })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Training failed.')
      setModelId(data.model_id); setFeatures(data.features || [])
      setFeatureTypes(data.feature_types || { numeric: [], categorical: [] })
      setTargetValues(data.classes || [])
      setValues(data.defaults || Object.fromEntries((data.features || []).map((feature) => [feature, ''])))
      setStatus(`Model trained · validation score ${(data.score * 100).toFixed(1)}%`)
    } catch (error) { setStatus(error.message.includes('Failed to fetch') ? 'API unavailable. Start the Python backend.' : error.message) }
  }
  const predict = async () => {
    if (!modelId) return setStatus('Train a model before checking a prediction.')
    if (features.some((feature) => values[feature] === undefined || values[feature] === '')) return setStatus('Enter a value for every feature before predicting.')
    try {
      const numericFeatures = new Set(featureTypes.numeric)
      const predictionValues = Object.fromEntries(Object.entries(values).map(([key, value]) => [key, numericFeatures.has(key) ? Number(value) : value]))
      const response = await fetch(`${API_URL}/models/predict`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ model_id: modelId, values: predictionValues }) })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Prediction failed.')
      setPrediction(String(data.prediction))
    } catch (error) { setStatus(error.message) }
  }
  const selectedFile = async (event) => {
    const file = event.target.files[0]
    if (!file) return
    const parsed = parseCsv(await file.text())
    const nextTarget = parsed.columns[parsed.columns.length - 1] || ''
    setDataset(file); setColumns(parsed.columns); setPreviewRows(parsed.rows); setTarget(nextTarget)
    setSelectedFeatures(parsed.columns.filter((column) => column !== nextTarget))
    setModelId(''); setFeatures([]); setFeatureTypes({ numeric: [], categorical: [] }); setTargetValues([]); setValues({}); setPrediction('')
  }
  const toggleFeature = (feature) => setSelectedFeatures((current) => current.includes(feature) ? current.filter((item) => item !== feature) : [...current, feature])
  return <><Hero icon={BrainCircuit} title="Model Maker" copy="Upload, inspect, clean, select features, train, and test a real scikit-learn model like the Streamlit workflow." /><section className="panel"><div className="panel-head"><div><h2>Upload your dataset</h2><p>Choose a CSV file to preview its columns and first 50 rows.</p></div><span className="eyebrow">CSV input</span></div><label className="dropzone compact"><input type="file" accept=".csv" onChange={selectedFile} /><UploadCloud size={23} /><strong>{dataset ? dataset.name : 'Upload a CSV dataset'}</strong><small>Numeric and categorical columns supported</small><span className="button">Choose CSV</span></label>{previewRows.length > 0 && <div className="csv-preview"><table><thead><tr>{columns.map((column) => <th key={column}>{column}</th>)}</tr></thead><tbody>{previewRows.map((row, rowIndex) => <tr key={rowIndex}>{columns.map((_, columnIndex) => <td key={columnIndex}>{row[columnIndex] || ''}</td>)}</tr>)}</tbody></table></div>}</section><div className="content-grid"><section className="panel"><div className="panel-head"><div><h2>Training configuration</h2><p>Select the target and learning method.</p></div><span className="eyebrow">Scikit-learn</span></div><Field label="Target variable"><select value={target} onChange={(event) => { setTarget(event.target.value); setSelectedFeatures(columns.filter((column) => column !== event.target.value)); setModelId('') }}><option value="">Select a target column</option>{columns.map((column) => <option key={column}>{column}</option>)}</select></Field><Field label="Learning method"><select value={method} onChange={(event) => setMethod(event.target.value)}><option>Random Forest Classifier</option><option>Logistic Regression</option><option>Linear Regression</option><option>Random Forest Regressor</option></select></Field><button className="primary" onClick={train}><BrainCircuit size={15} />Train model</button>{status && <div className="notice">{status}</div>}</section><section className="panel"><div className="panel-head"><div><h2>Feature selection</h2><p>Choose the columns used by the model.</p></div><span className="eyebrow">{selectedFeatures.length} selected</span></div>{columns.filter((column) => column !== target).map((feature) => <label className="feature" key={feature}><span>{feature}</span><input type="checkbox" checked={selectedFeatures.includes(feature)} onChange={() => toggleFeature(feature)} /></label>)}<Metric label="Target values" value={targetValues.length ? targetValues.join(' / ') : 'Detected after training'} /><Metric label="Validation split" value="80 / 20" /><Metric label="Pipeline" value="Impute + encode + model" /></section></div><section className="panel check-panel"><div className="panel-head"><div><h2>Check model</h2><p>Default values are filled from the dataset averages and most common categories.</p></div><span className="eyebrow">Live input</span></div><div className="two-col">{features.map((feature) => <Field label={feature} key={feature}><input type={featureTypes.numeric.includes(feature) ? 'number' : 'text'} value={values[feature] ?? ''} onChange={updateValue(feature)} /></Field>)}</div><div className="model-actions"><button className="primary" onClick={predict}><Send size={15} />Predict class</button>{modelId && <a className="button" href={`${API_URL}/models/${modelId}/download`} download>Download model</a>}</div>{prediction && <div className="result"><span>Predicted class</span><strong>{prediction}</strong><small>Prediction uses the original target value, such as Fraud, Not Fraud, Active, or Inactive.</small></div>}</section></>
}

export default function App() {
  const [loading, setLoading] = useState(true)
  const [user, setUser] = useState(() => JSON.parse(sessionStorage.getItem('researchOrbitUser') || 'null'))
  useEffect(() => { const timer = setTimeout(() => setLoading(false), 850); return () => clearTimeout(timer) }, [])
  const authenticate = (nextUser) => { sessionStorage.setItem('researchOrbitUser', JSON.stringify(nextUser)); setUser(nextUser) }
  const logout = () => { sessionStorage.removeItem('researchOrbitUser'); setUser(null) }
  if (loading) return <LoadingScreen />
  if (!user) return <Auth onAuth={authenticate} />
  return <Shell user={user} onLogout={logout} />
}
