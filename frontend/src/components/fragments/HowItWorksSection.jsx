import { CheckCircle2, Filter, LogIn, TimerReset } from "lucide-react";

const steps = [
  {
    title: "Input Preferensi",
    description: "Masukkan kebutuhan dan batasan budget.",
    icon: LogIn,
  },
  {
    title: "Proses Naive Bayes",
    description: "Klasifikasi data berdasarkan spesifikasi.",
    icon: TimerReset,
  },
  {
    title: "Penyaringan",
    description: "Filter hasil sesuai kriteria pengguna.",
    icon: Filter,
  },
  {
    title: "Hasil Rekomendasi",
    description: "Tampilkan laptop terbaik beserta alasan.",
    icon: CheckCircle2,
  },
];

function HowItWorksSection() {
  return (
    <section className="home-process">
      <div className="container-app">
        <div className="home-section-header">
          <h2
            className="home-section-title"
            data-aos="fade-up"
            data-aos-duration="800"
          >
            Cara Kerja Sistem
          </h2>
          <p
            className="home-section-description"
            data-aos="fade-up"
            data-aos-duration="1200"
          >
            Pendekatan berbasis data untuk memberikan rekomendasi yang presisi.
          </p>
        </div>

        <div className="home-step-grid">
          {steps.map((step, index) => {
            const Icon = step.icon;

            return (
              <article className="home-step" key={step.title}>
                <span className="home-step-number">{index + 1}</span>
                <div
                  className="home-step-card"
                  data-aos="fade-up"
                  data-aos-duration="800"
                >
                  <Icon
                    aria-hidden="true"
                    className="home-step-icon"
                    size={20}
                  />
                  <h3 className="home-step-title">{step.title}</h3>
                  <p className="home-step-description">{step.description}</p>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default HowItWorksSection;
