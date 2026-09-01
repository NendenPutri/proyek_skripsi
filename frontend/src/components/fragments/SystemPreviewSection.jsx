import { ArrowRight, CheckCircle2, Cpu, HardDrive, Laptop, MemoryStick, Monitor } from 'lucide-react'

function PreviewInput({ label, value, active = false }) {
  return (
    <div className="preview-input-group">
      <span>{label}</span>
      <div className={active ? 'preview-input preview-input-active' : 'preview-input'}>
        <span>{value}</span>
        {active ? <CheckCircle2 aria-hidden="true" size={16} /> : null}
      </div>
    </div>
  )
}

function SystemPreviewSection() {
  return (
    <section className="landing-preview-section">
      <div className="container-app">
        <header className="home-section-header">
          <h2
            className="home-section-title"
            data-aos="fade-up"
            data-aos-duration="800"
          >
            Preview Sistem Rekomendasi
          </h2>
          <p
            className="home-section-description"
            data-aos="fade-up"
            data-aos-duration="1200"
          >
            Lihat bagaimana sistem mencocokkan kriteria pengguna dengan hasil
            rekomendasi yang paling mendekati.
          </p>
        </header>

        <div
          className="preview-panel"
          data-aos="zoom-in"
          data-aos-duration="1200"
        >
          <div className="preview-form-card">
            <span className="preview-sticker">Input Anda</span>
            <PreviewInput active label="Kebutuhan Utama" value="Programming" />
            <PreviewInput label="Budget Maksimal" value="Rp 8.000.000" />
            <PreviewInput label="Preferensi Brand" value="Semua Brand" />
            <div className="preview-processing">Memproses Data...</div>
          </div>

          <div className="preview-arrow">
            <ArrowRight aria-hidden="true" size={34} />
          </div>

          <div className="preview-result-card">
            <span className="preview-match">98% Match</span>
            <div className="preview-result-content">
              <div className="preview-laptop-icon">
                <Laptop aria-hidden="true" size={42} />
              </div>
              <div className="preview-result-body">
                <h3>ASUS Vivobook 14</h3>
                <p className="preview-price">Rp 7.499.000</p>
                <div className="preview-spec-grid">
                  <span>
                    <Cpu aria-hidden="true" size={15} />
                    Intel Core i5
                  </span>
                  <span>
                    <MemoryStick aria-hidden="true" size={15} />
                    8GB RAM
                  </span>
                  <span>
                    <HardDrive aria-hidden="true" size={15} />
                    512GB SSD
                  </span>
                  <span>
                    <Monitor aria-hidden="true" size={15} />
                    Integrated GPU
                  </span>
                </div>
                <div className="preview-reason">
                  <strong>Alasan Rekomendasi:</strong>
                  <p>
                    Spesifikasi CPU dan RAM memadai untuk menjalankan IDE,
                    kompilasi kode, dan proyek development. Harga berada di
                    bawah batas budget.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default SystemPreviewSection
