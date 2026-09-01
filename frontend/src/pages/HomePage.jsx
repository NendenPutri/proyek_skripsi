import {
  FeatureSection,
  FinalCtaSection,
  HeroSection,
  HowItWorksSection,
  NeedCategorySection,
  SystemPreviewSection,
  WhyLaptopWiseSection,
  MessageLaptop
} from '../components/fragments'

function HomePage() {
  return (
    <div className="home-page">
      <HeroSection />
      <MessageLaptop/>
      <FeatureSection />
      <HowItWorksSection />
      <NeedCategorySection />
      <SystemPreviewSection />
      <WhyLaptopWiseSection />
      <FinalCtaSection />
    </div>
  )
}

export default HomePage
