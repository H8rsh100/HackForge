import { useState } from 'react';
import FileUpload from './components/FileUpload';
import History from './components/History';
import Navbar from './components/Navbar'; // I see this in your sidebar!
import './App.css';

function App() {
  // This state is the "trigger" for Brick 7
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleNewUpload = () => {
    // Incrementing this value tells the History component to refresh
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="App">
      <Navbar />
      <div className="container" style={{ padding: '2rem' }}>
        <header>
          <h1>EcoTrack AI 🌿</h1>
          <p>Real-time Sustainability Tracking</p>
        </header>

        <main>
          {/* We pass handleNewUpload as a "prop" to FileUpload */}
          <FileUpload onUploadSuccess={handleNewUpload} />
          
          <hr style={{ margin: '3rem 0', opacity: 0.2 }} />

          {/* We pass the trigger to History */}
          <History refreshKey={refreshTrigger} />
        </main>
      </div>
    </div>
  );
}

export default App;