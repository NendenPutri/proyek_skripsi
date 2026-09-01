import { Brush, Code2, FileText, Video } from 'lucide-react'

const categories = [
  {
    title: 'Administrasi',
    description:
      'Cocok untuk dokumen, spreadsheet, browsing, meeting online, dan pekerjaan ringan.',
    icon: FileText,
    iconClass: 'landing-icon-blue',
    tags: ['RAM 4-8GB', 'Integrated GPU'],
  },
  {
    title: 'Programming',
    description:
      'Multitasking lancar untuk coding, IDE, database lokal, dan web development.',
    icon: Code2,
    iconClass: 'landing-icon-green',
    tags: ['RAM 8-16GB', 'SSD 512GB+'],
  },
  {
    title: 'Desain Grafis',
    description:
      'Performa visual yang baik untuk UI design, editing gambar, dan aplikasi kreatif.',
    icon: Brush,
    iconClass: 'landing-icon-pink',
    tags: ['Color Accurate Screen', 'GPU Dedicated'],
  },
  {
    title: 'Editing Video',
    description:
      'Tenaga komputasi maksimal untuk rendering cepat dan editing video resolusi tinggi.',
    icon: Video,
    iconClass: 'landing-icon-yellow',
    tags: ['High-End CPU', 'GPU Dedicated', 'RAM 16GB+'],
  },
]

function NeedCategorySection() {
  return (
    <section className="landing-category-section">
      <div className="container-app">
        <div className="landing-split">
          <div className="landing-split-copy">
            <h2
              className="landing-split-title"
              data-aos="fade-up"
              data-aos-duration="800"
            >
              Kategori Kebutuhan Laptop
            </h2>
            <p
              className="landing-split-description"
              data-aos="fade-up"
              data-aos-duration="1200"
            >
              Setiap kebutuhan komputasi memiliki standar spesifikasi yang berbeda.
              Sistem mengelompokkan rekomendasi berdasarkan parameter ideal untuk
              aktivitas utama agar perangkat bekerja optimal tanpa over-budget.
            </p>
          </div>

          <div className="landing-category-grid">
            {categories.map((category) => {
              const Icon = category.icon

              return (
                <article
                  className="landing-category-card"
                  data-aos="zoom-in"
                  data-aos-duration="1200"
                  key={category.title}
                >
                  <div className="landing-category-heading">
                    <span className={`landing-category-icon ${category.iconClass}`}>
                      <Icon aria-hidden="true" size={22} />
                    </span>
                    <h3>{category.title}</h3>
                  </div>
                  <p>{category.description}</p>
                  <div className="landing-tag-list">
                    {category.tags.map((tag) => (
                      <span className="landing-tag" key={tag}>
                        {tag}
                      </span>
                    ))}
                  </div>
                </article>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}

export default NeedCategorySection
