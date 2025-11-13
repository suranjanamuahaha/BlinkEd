import { useState } from "react";

export default function HomePage() {
    const [prompt, setPrompt] = useState("");
    const [videoUrl, setVideoUrl] = useState(null);
    const [resourceLinks, setResourceLinks] = useState([]);
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const handleSend = () => {
        if (!prompt.trim()) return;

        setVideoUrl("https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4");
        setResourceLinks([
            "https://en.wikipedia.org/wiki/Photosynthesis",
            "https://www.khanacademy.org/science/biology",
        ]);
    };

    return (
        <div className="h-screen w-screen flex bg-gray-100 text-gray-900">

            {/* Sidebar */}
            <aside className="w-64 bg-white shadow-lg p-4 flex flex-col">
                <h1 className="text-xl font-bold mb-4">BlinkEd</h1>

                <button className="bg-blue-600 text-white p-2 rounded mb-3">
                    + New Video
                </button>

                <h2 className="text-sm uppercase font-semibold text-gray-500 mb-2">
                    Chat History
                </h2>

                <div className="flex-1 overflow-y-auto space-y-2">
                    <div className="p-2 bg-gray-200 rounded cursor-pointer">Photosynthesis</div>
                    <div className="p-2 bg-gray-200 rounded cursor-pointer">What is BMI?</div>
                    <div className="p-2 bg-gray-200 rounded cursor-pointer">How to start sewing?</div>
                </div>
            </aside>

            {/* Main Area */}
            <main className="flex-1 flex flex-col">

                {/* Navbar */}
                <div className="w-full h-14 border-b bg-white flex items-center justify-between px-4">
                    <h2 className="font-semibold text-lg">AI Explainer</h2>

                    {!isLoggedIn ? (
                        <button className="px-4 py-1 bg-blue-600 text-white rounded">
                            Login / Signup
                        </button>
                    ) : (
                        <div className="w-10 h-10 rounded-full bg-gray-300 cursor-pointer"></div>
                    )}
                </div>

                {/* Chat Output */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    {videoUrl && (
                        <div className="bg-white p-4 rounded shadow">
                            <h3 className="font-semibold mb-2">Generated Video</h3>

                            <video
                                controls
                                className="rounded mb-4 w-full max-w-xl"
                                src={videoUrl}
                            />

                            <h4 className="font-semibold">Sources:</h4>
                            <ul className="list-disc pl-6 text-blue-600">
                                {resourceLinks.map((link, i) => (
                                    <li key={i}>
                                        <a href={link} target="_blank">
                                            {link}
                                        </a>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                {/* Chat Input */}
                <div className="w-full border-t bg-white p-4">
                    <div className="flex items-center gap-2">
                        <input
                            type="text"
                            placeholder="Ask BlinkEd anything..."
                            className="flex-1 p-3 rounded border outline-none focus:ring-2 focus:ring-blue-500"
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                        />

                        <button
                            onClick={handleSend}
                            className="px-4 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
                        >
                            Generate
                        </button>
                    </div>
                </div>

            </main>
        </div>
    );
}
