import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex flex-col items-center justify-center text-white p-4">
      <header className="text-center mb-12">
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-4">
          CreditBPO Matching Platform
        </h1>
        <p className="text-xl md:text-2xl font-light max-w-2xl mx-auto">
          Connecting Business Service Seekers with Expert Providers Effortlessly.
        </p>
      </header>
      <main className="flex flex-col md:flex-row items-center gap-8">
        <Link
          href="/login"
          className="px-10 py-4 bg-white text-indigo-600 font-semibold rounded-lg shadow-lg hover:bg-gray-100 transition-colors text-lg transform hover:scale-105"
        >
          Login
        </Link>
        <Link
          href="/signup"
          className="px-10 py-4 bg-transparent border-2 border-white text-white font-semibold rounded-lg shadow-lg hover:bg-white hover:text-pink-500 transition-colors text-lg transform hover:scale-105"
        >
          Sign Up
        </Link>
      </main>
      <section className="mt-20 max-w-4xl text-center">
        <h2 className="text-3xl font-bold mb-6">Why Choose Us?</h2>
        <div className="grid md:grid-cols-3 gap-8 text-left">
          <div className="bg-white/20 backdrop-blur-md p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-2">Smart Matching</h3>
            <p className="text-sm">Our intelligent algorithm connects you with the most relevant partners based on your specific needs.</p>
          </div>
          <div className="bg-white/20 backdrop-blur-md p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-2">Verified Profiles</h3>
            <p className="text-sm">Trust and transparency are key. We ensure profiles are vetted for quality and reliability.</p>
          </div>
          <div className="bg-white/20 backdrop-blur-md p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-2">Streamlined Process</h3>
            <p className="text-sm">From finding a match to project completion, our platform simplifies every step.</p>
          </div>
        </div>
      </section>
      <footer className="absolute bottom-8 text-center text-sm text-white/80">
        © {new Date().getFullYear()} CreditBPO Matching Platform. Find your perfect business partner today.
      </footer>
    </div>
  );
}