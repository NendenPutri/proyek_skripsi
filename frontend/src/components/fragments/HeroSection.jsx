import { ArrowRight, BarChart3, Cpu, Star } from "lucide-react";
import { Link } from "react-router-dom";
// import HealthStatus from './HealthStatus'

function HeroSection() {
  return (
    <section className="home-hero">
      <div className="hero-orbit hero-orbit-outer"  />
      <div className="hero-orbit hero-orbit-middle" />
      <div className="hero-orbit hero-orbit-core" />

      <span className="hero-float hero-float-cpu animate-[bounce_3s_ease-in-out_infinite]">
        <Cpu aria-hidden="true" size={24} />
      </span>
      <span className="hero-float hero-float-star animate-[bounce_2.5s_ease-in-out_infinite]">
        <Star aria-hidden="true" size={28} />
      </span>
      <span className="hero-float hero-float-chart animate-[bounce_3.5s_ease-in-out_infinite]">
        <BarChart3 aria-hidden="true" size={22} />
      </span>

      <div className="hero-content">
        <h1
          className="home-hero-title"
          data-aos="zoom-in"
          data-aos-duration="1000"
        >
          <span className="hero-title-line">
            Temukan <span className="hero-highlight">Laptop</span>
          </span>
          <span className="hero-title-line">
            Sesuai <span className="hero-highlight">Kebutuhanmu</span>
          </span>
        </h1>
        <p
          className="home-hero-description"
          data-aos="zoom-in"
          data-aos-duration="1800"
        >
          Pilih kebutuhan penggunaan, tentukan budget, lalu sistem akan
          menampilkan rekomendasi laptop berdasarkan spesifikasi, harga, dan
          hasil klasifikasi Naive Bayes.
        </p>
        <div className="home-hero-actions">
          <Link
            className="home-btn-primary"
            to="/recommendation"
            data-aos="fade-up"
            data-aos-duration="1500"
          >
            Mulai Rekomendasi
          </Link>
          <Link
            className="home-btn-secondary"
            to="/about"
            data-aos="fade-up"
            data-aos-duration="1800"
          >
            Explore Demo
            <ArrowRight aria-hidden="true" size={16} />
          </Link>
        </div>
        {/* <div className="hero-status animate-pulse">
          <HealthStatus />
        </div> */}
      </div>
    </section>
  );
}

export default HeroSection;
