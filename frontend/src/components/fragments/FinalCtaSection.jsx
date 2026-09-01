import { Link } from 'react-router-dom'

function FinalCtaSection() {
  return (
    <section className="landing-cta-section">
      <div className="container-app">
        <div
          className="landing-cta-card"
          data-aos="zoom-in"
          data-aos-duration="1200"
        >
          <h2>Siap Menemukan Laptop yang Sesuai?</h2>
          <p>
            Mulai isi kebutuhan dan preferensi Anda, lalu lihat rekomendasi
            laptop yang paling mendekati secara cepat dan akurat.
          </p>
          <Link
            className="home-btn-primary landing-cta-button"
            to="/recommendation"
          >
            Mulai Rekomendasi Sekarang
          </Link>
          <span>Akses instan. Tanpa perlu mendaftar akun.</span>
        </div>
      </div>
    </section>
  )
}

export default FinalCtaSection
