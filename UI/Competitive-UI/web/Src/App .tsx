import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import Governance from './pages/Governance';
import Analysis from './pages/Analysis';
import Generation from './pages/Generation';
import Foresight from './pages/Foresight';
import Law from './pages/Law';
import Medicine from './pages/Medicine';
import Agriculture from './pages/Agriculture';
import Settings from './pages/Settings';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/governance" element={<Governance />} />
            <Route path="/analysis" element={<Analysis />} />
            <Route path="/generation" element={<Generation />} />
            <Route path="/foresight" element={<Foresight />} />
            <Route path="/law" element={<Law />} />
            <Route path="/medicine" element={<Medicine />} />
            <Route path="/agriculture" element={<Agriculture />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </Router>
      <Toaster position="top-right" />
    </QueryClientProvider>
  );
}

export default App;
