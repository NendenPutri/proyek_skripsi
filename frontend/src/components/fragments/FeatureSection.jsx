import {
  Blocks,
  ClipboardCheck,
  SlidersHorizontal,
  Sparkles,
} from "lucide-react";

const features = [
  {
    title: "Rekomendasi Berdasarkan Kebutuhan",
    description:
      "Sistem mengelompokkan laptop ke dalam kategori administrasi, programming, desain grafis, dan editing video.",
    icon: Sparkles,
    tone: "pink",
  },
  {
    title: "Filter Budget dan Spesifikasi",
    description:
      "Pengguna dapat menyesuaikan budget, RAM, storage, processor, GPU, brand, dan sistem operasi.",
    icon: SlidersHorizontal,
    tone: "yellow",
  },
  {
    title: "Hasil dengan Alasan",
    description:
      "Setiap rekomendasi dilengkapi spesifikasi utama dan alasan mengapa laptop tersebut cocok.",
    icon: ClipboardCheck,
    tone: "blue",
  },
  {
    title: "Data Rekomendasi Terpusat",
    description: "Rekomendasi ditampilkan dari data laptop yang dikelola secara terpusat.",
    icon: Blocks,
    tone: "green",
  },
];

function FeatureSection() {
  return (
    <section className="home-features">
      <div className="container-app">
        <div className="home-section-header">
          <span
            className="section-kicker"
            data-aos="fade-up"
            data-aos-duration="500"
          >
            Fitur
          </span>
          <h2
            className="home-section-title"
            data-aos="fade-up"
            data-aos-duration="1200"
          >
            Fitur Cerdas untuk Anda
          </h2>
        </div>

        <div className="home-feature-grid">
          {features.map((feature) => {
            const Icon = feature.icon;

            return (
              <article
                data-aos="zoom-in"
                data-aos-duration="1200"
                className="home-feature-card"
                key={feature.title}
              >
                <span
                  className={`home-feature-icon feature-icon-${feature.tone}`}
                >
                  <Icon aria-hidden="true" size={24} />
                </span>
                <h3 className="home-card-title">{feature.title}</h3>
                <p className="home-card-description">{feature.description}</p>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default FeatureSection;
