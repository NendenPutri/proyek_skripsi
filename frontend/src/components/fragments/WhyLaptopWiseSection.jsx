import { Brain, CheckCircle2, Database, Lightbulb, SlidersHorizontal, Sparkles } from 'lucide-react'

const pipelineSteps = [
  { label: 'Dataset Laptop', icon: Database, state: 'primary' },
  { label: 'Preprocessing Data', icon: Sparkles, state: 'primary' },
  { label: 'Model Naive Bayes', icon: Brain, state: 'highlight' },
  { label: 'Filter & Ranking', icon: SlidersHorizontal, state: 'primary' },
  { label: 'Rekomendasi Final', icon: CheckCircle2, state: 'success' },
]

const reasons = [
  {
    title: 'Berbasis Dataset',
    description:
      'Rekomendasi diolah dari dataset spesifikasi laptop yang telah melalui proses pembersihan data.',
    icon: Database,
    iconClass: 'landing-icon-blue',
  },
  {
    title: 'Klasifikasi Naive Bayes',
    description:
      'Model machine learning memetakan spesifikasi teknis ke kategori penggunaan secara terukur.',
    icon: Brain,
    iconClass: 'landing-icon-pink',
  },
  {
    title: 'Filter Presisi',
    description:
      'Hasil dapat disesuaikan dengan budget, brand, RAM, storage, GPU, dan sistem operasi.',
    icon: SlidersHorizontal,
    iconClass: 'landing-icon-yellow',
  },
  {
    title: 'Alasan Rekomendasi',
    description:
      'Sistem tidak hanya menampilkan laptop, tetapi juga menjelaskan alasan kecocokannya.',
    icon: Lightbulb,
    iconClass: 'landing-icon-green',
  },
]

function WhyLaptopWiseSection() {
  return (
    <section className="landing-why-section">
      <div className="container-app">
        <div className="landing-why-grid">
          <div className="pipeline-list">
            {pipelineSteps.map((step) => {
              const Icon = step.icon

              return (
                <div
                  className={`pipeline-step pipeline-step-${step.state}`}
                  data-aos="fade-up"
                  data-aos-duration="800"
                  key={step.label}
                >
                  <span className="pipeline-dot" />
                  <div className="pipeline-card">
                    <Icon aria-hidden="true" size={18} />
                    <span>{step.label}</span>
                  </div>
                </div>
              )
            })}
          </div>

          <div>
            <h2
              className="landing-split-title"
              data-aos="fade-up"
              data-aos-duration="800"
            >
              Kenapa LaptopWise?
            </h2>
            <div className="landing-reason-grid">
              {reasons.map((reason) => {
                const Icon = reason.icon

                return (
                  <article
                    className="landing-reason-card"
                    data-aos="zoom-in"
                    data-aos-duration="1200"
                    key={reason.title}
                  >
                    <span className={`landing-reason-icon ${reason.iconClass}`}>
                      <Icon aria-hidden="true" size={20} />
                    </span>
                    <h3>{reason.title}</h3>
                    <p>{reason.description}</p>
                  </article>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default WhyLaptopWiseSection
