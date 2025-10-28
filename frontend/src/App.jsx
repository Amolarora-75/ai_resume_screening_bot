
import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import clsx from 'clsx'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Header() {
  return (
    <div className="max-w-5xl mx-auto pt-10 pb-6">
      <h1 className="text-4xl font-extrabold tracking-tight flex items-center gap-2">
        <span className="inline-block bg-indigo-600 p-2 rounded-xl">📄</span>
        Resume Screening AI Bot
      </h1>
    </div>
  )
}

function Tabs({tab, setTab}) {
  return (
    <div className="max-w-5xl mx-auto flex gap-3">
      <button className={clsx('tab', tab==='upload' ? 'tab-active':'' )} onClick={()=>setTab('upload')}>Upload</button>
      <button className={clsx('tab', tab==='history' ? 'tab-active':'' )} onClick={()=>setTab('history')}>History</button>
    </div>
  )
}

function UploadTab() {
  const [job, setJob] = useState('')
  const [files, setFiles] = useState([])
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState(null)

  const onDrop = (e)=>{
    e.preventDefault()
    const items = Array.from(e.dataTransfer.files).filter(f=>f.type==='application/pdf')
    setFiles(prev => [...prev, ...items])
  }

  const onChangeFiles = (e)=>{
    const items = Array.from(e.target.files).filter(f=>f.type==='application/pdf')
    setFiles(prev => [...prev, ...items])
  }

  const removeFile = (idx)=> setFiles(prev => prev.filter((_,i)=>i!==idx))

  const submit = async ()=>{
    if (!files.length) return alert('Please add at least one PDF.')
    setBusy(true)
    try{
      const form = new FormData()
      form.append('job_description', job)
      files.forEach(f => form.append('files', f))

      const {data} = await axios.post(`${API}/api/parse`, form)
      setResult(data)
      setFiles([])
    }catch(err){
      console.error(err)
      alert('Upload failed. Is the API running at '+API+'?')
    }finally{ setBusy(false) }
  }

  return (
    <div className="max-w-5xl mx-auto mt-6 grid gap-6">
      <div className="card p-4">
        <div className="text-sm text-neutral-300 mb-2">Job Description (Max 1000 words)</div>
        <textarea value={job} onChange={e=>setJob(e.target.value)} rows={8} className="w-full p-3" placeholder="Paste the JD here..." />
      </div>

      <div className="card p-4">
        <div className="text-sm mb-2">Upload Resume PDFs</div>
        <div onDragOver={(e)=>e.preventDefault()} onDrop={onDrop} className="upload-box">
          <div className="text-neutral-300">Drag and drop files here</div>
          <div className="text-xs text-neutral-400">Limit 200MB per file • PDF</div>
          <label className="button mt-2 cursor-pointer">
            <input type="file" multiple accept="application/pdf" className="hidden" onChange={onChangeFiles} />
            Browse files
          </label>
        </div>

        {files.length>0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {files.map((f,idx)=>(
              <div key={idx} className="px-3 py-2 bg-neutral-700 rounded-xl flex items-center gap-2 text-sm">
                <span>{f.name}</span>
                <button className="text-red-400" onClick={()=>removeFile(idx)}>✕</button>
              </div>
            ))}
          </div>
        )}

        <button disabled={busy} onClick={submit} className="button mt-4">{busy?'Uploading...':'Upload at least one resume PDF.'}</button>
      </div>

      {result && (
        <div className="card p-4">
          <div className="text-lg font-semibold mb-2">Parsed</div>
          <pre className="bg-neutral-900 rounded-xl p-3 overflow-auto text-xs">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

function HistoryTab(){
  const [rows, setRows] = useState([])
  const [open, setOpen] = useState(null)

  const fetchRows = async ()=>{
    try{
      const {data} = await axios.get(`${API}/api/resumes`)
      setRows(data)
    }catch(e){ console.error(e) }
  }

  useEffect(()=>{ fetchRows() }, [])

  return (
    <div className="max-w-5xl mx-auto mt-6">
      <div className="card p-4">
        <div className="overflow-auto">
          <table className="table w-full">
            <thead className="text-left text-neutral-300">
              <tr>
                <th>File</th><th>Name</th><th>Email</th><th>Phone</th><th>Rating</th><th></th>
              </tr>
            </thead>
            <tbody>
              {rows.map(r=>(
                <tr key={r.id} className="border-t border-neutral-700">
                  <td>{r.file_name}</td>
                  <td>{r.name || '-'}</td>
                  <td>{r.email || '-'}</td>
                  <td>{r.phone || '-'}</td>
                  <td>{r.resume_rating ?? '-'}</td>
                  <td><button className="button" onClick={()=>setOpen(r.id)}>Details</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {open && <DetailsModal id={open} onClose={()=>setOpen(null)} />}
    </div>
  )
}

function DetailsModal({id, onClose}){
  const [data, setData] = useState(null)
  useEffect(()=>{
    (async ()=>{
      try{
        const res = await axios.get(`${API}/api/resumes/${id}`)
        setData(res.data)
      }catch(e){ console.error(e) }
    })()
  },[id])

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-card" onClick={(e)=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold">Resume Details</h3>
          <button onClick={onClose} className="text-neutral-400">✕</button>
        </div>
        {!data ? <div>Loading...</div> : (
          <div className="grid gap-3">
            <div><span className="text-neutral-400">Name:</span> {data.name || '-'}</div>
            <div><span className="text-neutral-400">Email:</span> {data.email || '-'}</div>
            <div><span className="text-neutral-400">Phone:</span> {data.phone || '-'}</div>
            <div><span className="text-neutral-400">Core Skills:</span> {data.core_skills?.join(', ')}</div>
            <div><span className="text-neutral-400">Rating:</span> {data.resume_rating ?? '-'}</div>
            <div>
              <div className="text-neutral-300 font-medium">Improvement Areas</div>
              <pre className="bg-neutral-800 p-3 rounded-xl whitespace-pre-wrap">{data.improvement_areas || '-'}</pre>
            </div>
            <div>
              <div className="text-neutral-300 font-medium">Upskill Suggestions</div>
              <pre className="bg-neutral-800 p-3 rounded-xl whitespace-pre-wrap">{data.upskill_suggestions || '-'}</pre>
            </div>
            <div>
              <div className="text-neutral-300 font-medium mb-1">Raw Extract (truncated)</div>
              <pre className="bg-neutral-950 p-3 rounded-xl text-xs max-h-64 overflow-auto">{(data.raw_text||'').slice(0,5000)}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default function App(){
  const [tab, setTab] = useState('upload')
  return (
    <div>
      <Header/>
      <Tabs tab={tab} setTab={setTab}/>
      {tab==='upload' ? <UploadTab/> : <HistoryTab/>}
    </div>
  )
}
