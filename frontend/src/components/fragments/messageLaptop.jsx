import Laptop from "../../assets/laptop.webp";

const MessageLaptop = () => {
  return (
    <section className="relative px-4 md:px-0 -mt-12 flex-col flex w-full max-w-5xl! mx-auto ">
      <div className="flex p-4 w-full max-w-3xs md:max-w-3xl bg-home-text gap-4 mx-auto items-center rounded-md text-center -mb-7 z-10">
        <p className="relative  font-caveat text-[18px] md:text-3xl  text-white">
          <span className="hero-highlight leading-3 font-bold text-black">
            Laptop
          </span>{" "}
          yang tepat bukan yang paling mahal, tetapi yang paling sesuai dengan
          kebutuhanmu.
        </p>
      </div>
      <img
        src={Laptop}
        alt="photo laptop"
        className="w-fit object-cover rounded-md"
        data-aos="fade-up"
        data-aos-duration="1000"
      />
    </section>
  );
};
export default MessageLaptop;
