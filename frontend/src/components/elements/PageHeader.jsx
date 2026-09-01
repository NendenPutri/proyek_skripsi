function PageHeader({ eyebrow, title, description }) {
  return (
    <div className="mb-8 max-w-3xl">
      {eyebrow ? <p className="text-sm font-bold uppercase tracking-wide text-indigo-600">{eyebrow}</p> : null}
      <h1 className="page-title">{title}</h1>
      {description ? <p className="mt-3 text-lg text-slate-600">{description}</p> : null}
    </div>
  )
}

export default PageHeader
