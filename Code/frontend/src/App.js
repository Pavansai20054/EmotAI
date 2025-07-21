import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useSpring, animated, useTransition } from "react-spring";
import styled from "styled-components";
import ParticleSystem from "./components/ParticleSystem";
import "./App.css";

// Styled Components with neon effects
const AppContainer = styled(motion.div)`
  min-height: 100vh;
  padding: 20px;
  font-family: 'Exo 2', sans-serif;
  color: #ffffff;
  position: relative;
  overflow-x: hidden;
`;

const GlowCard = styled(motion.div)`
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid ${props => props.borderColor || '#00ffff'};
  border-radius: 15px;
  padding: 30px;
  box-shadow: 
    0 0 30px ${props => props.glowColor || 'rgba(0, 255, 255, 0.2)'},
    inset 0 0 30px ${props => props.glowColor || 'rgba(0, 255, 255, 0.05)'};
  backdrop-filter: blur(15px);
  position: relative;
  margin: 20px auto;
  max-width: 800px;
`;

const NeonText = styled(motion.h1)`
  font-family: 'Orbitron', monospace;
  font-size: 3.5rem;
  font-weight: 900;
  text-align: center;
  margin: 40px 0;
  background: linear-gradient(45deg, #00ffff, #ff00ff, #00ff00);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 3s ease-in-out infinite;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const FloatingParticle = styled(motion.div)`
  position: absolute;
  width: 4px;
  height: 4px;
  background: ${props => props.color};
  border-radius: 50%;
  box-shadow: 0 0 10px ${props => props.color};
`;

function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [particles, setParticles] = useState([]);
  const [feedback, setFeedback] = useState("");
  const [rating, setRating] = useState(5);
  const [analytics, setAnalytics] = useState(null);

  // Floating particles
  useEffect(() => {
    const colors = ['#00ffff', '#ff00ff', '#00ff00', '#ffff00', '#ff0080'];
    const newParticles = Array.from({ length: 20 }, (_, i) => ({
      id: i,
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      color: colors[Math.floor(Math.random() * colors.length)],
    }));
    setParticles(newParticles);
  }, []);

  // Spring animation for main container
  const containerSpring = useSpring({
    from: { opacity: 0, transform: 'translateY(50px)' },
    to: { opacity: 1, transform: 'translateY(0px)' },
    config: { tension: 280, friction: 60 }
  });

  // Transitions for result display
  const resultTransitions = useTransition(result, {
    from: { opacity: 0, transform: 'scale(0.8) rotateX(-90deg)' },
    enter: { opacity: 1, transform: 'scale(1) rotateX(0deg)' },
    leave: { opacity: 0, transform: 'scale(0.8) rotateX(90deg)' },
    config: { tension: 300, friction: 30 }
  });

  // Suggest emoji handler with loading animation
  const handleSuggest = async () => {
    if (!message.trim()) {
      setError("Please enter your message.");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);
    
    try {
      const res = await fetch("/suggest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      
      if (!res.ok) {
        throw new Error("Backend error: " + res.status);
      }
      
      const data = await res.json();
      
      setTimeout(() => {
        setResult(data);
        setLoading(false);
        handleShowHistory(); // Refresh history after suggestion
      }, 1000);
      
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // Show history handler (no username needed)
  const handleShowHistory = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`/history`);
      if (!res.ok) {
        throw new Error("Backend error: " + res.status);
      }
      const data = await res.json();
      setTimeout(() => {
        setHistory(Array.isArray(data.history) ? data.history : []);
        setLoading(false);
      }, 800);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // Analytics fetch
  const handleAnalytics = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await fetch("/analytics");
      if (!res.ok) {
        throw new Error("Backend error: " + res.status);
      }
      const data = await res.json();
      setTimeout(() => {
        setAnalytics(data.emoji_usage || []);
        setLoading(false);
      }, 800);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // Feedback submission
  const handleFeedback = async () => {
    if (!message.trim()) return;
    try {
      await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, feedback, rating }),
      });
      setFeedback(""); setRating(5);
      alert("Thank you for your feedback!");
    } catch (err) {
      alert("Failed to submit feedback");
    }
  };

  // Auto-load history on mount
  useEffect(() => {
    handleShowHistory();
    // eslint-disable-next-line
  }, []);

  const clearAll = () => {
    setMessage("");
    setResult(null);
    setHistory([]);
    setFeedback("");
    setRating(5);
    setError("");
    setAnalytics(null);
  };

  // Helper function to safely render emojis
  const renderEmojis = (emojis) => {
    if (!emojis) return "No emojis";
    if (Array.isArray(emojis)) return emojis.join(" ");
    return emojis;
  };

  return (
    <animated.div style={containerSpring}>
      <ParticleSystem />
      <AppContainer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        {/* Floating Particles */}
        {particles.map((particle) => (
          <FloatingParticle
            key={particle.id}
            color={particle.color}
            initial={{ x: particle.x, y: particle.y }}
            animate={{
              x: particle.x + Math.sin(Date.now() * 0.001 + particle.id) * 100,
              y: particle.y + Math.cos(Date.now() * 0.001 + particle.id) * 100,
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              repeatType: "reverse",
              ease: "easeInOut"
            }}
          />
        ))}

        {/* Main Title */}
        <NeonText
          initial={{ y: -100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, delay: 0.2 }}
          data-text="EmotAI"
          className="glitch"
        >
          EmotAI
        </NeonText>

        {/* Input Section */}
        <motion.div 
          className="input-container"
          initial={{ x: -200, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <motion.input
            className="neon-input"
            placeholder="Enter your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                handleSuggest();
              }
            }}
            whileFocus={{ scale: 1.02 }}
            transition={{ type: "spring", stiffness: 300 }}
          />
        </motion.div>

        {/* Button Section */}
        <motion.div 
          className="button-container"
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <motion.button
            className="neon-button"
            onClick={handleSuggest}
            disabled={loading}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            {loading ? "Processing..." : "Suggest Emoji"}
          </motion.button>
          
          <motion.button
            className="neon-button"
            onClick={handleShowHistory}
            disabled={loading}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            Show History
          </motion.button>
          
          <motion.button
            className="neon-button"
            onClick={clearAll}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            transition={{ type: "spring", stiffness: 400 }}
            style={{ background: 'linear-gradient(45deg, #ff4444, #ff0000)' }}
          >
            Clear All
          </motion.button>
        </motion.div>

        {/* Analytics Button */}
        <div style={{ margin: "20px 0" }}>
          <button className="neon-button" onClick={handleAnalytics} disabled={loading}>
            Show Emoji Analytics
          </button>
        </div>
        {analytics && (
          <GlowCard borderColor="#00ff00" glowColor="rgba(0,255,0,0.2)">
            <div className="analytics-title">Emoji Usage Stats</div>
            <ul>
              {analytics.map(({emoji, count}) => (
                <li key={emoji}>{emoji}: {count}</li>
              ))}
            </ul>
          </GlowCard>
        )}

        {/* Loading Spinner */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0 }}
              transition={{ duration: 0.3 }}
              style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}
            >
              <div className="loading-spinner"></div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Result Display & Feedback Form */}
        {resultTransitions((style, item) =>
          item && (
            <animated.div style={style}>
              <GlowCard
                borderColor="#00ffff"
                glowColor="rgba(0, 255, 255, 0.3)"
                initial={{ rotateY: -90, opacity: 0 }}
                animate={{ rotateY: 0, opacity: 1 }}
                transition={{ duration: 0.8 }}
              >
                <div className="result-title">AI Suggestion</div>
                <motion.div 
                  className="emoji-display"
                  animate={{ 
                    scale: [1, 1.2, 1],
                    rotate: [0, 5, -5, 0]
                  }}
                  transition={{ 
                    duration: 2,
                    repeat: Infinity,
                    repeatType: "reverse"
                  }}
                >
                  {renderEmojis(item?.emojis)}
                </motion.div>
                <div className="explanation-text">
                  <strong>Explanation:</strong> {item?.explanation || "No explanation available"}
                </div>
              </GlowCard>
              
              {/* Feedback Form - ONLY show after result */}
              <GlowCard borderColor="#ff00ff" glowColor="rgba(255,0,255,0.15)">
                <div className="feedback-title">Feedback</div>
                <textarea
                  className="feedback-textarea"
                  value={feedback}
                  onChange={e => setFeedback(e.target.value)}
                  placeholder="Your feedback on emoji suggestion (optional)"
                  style={{ width: "100%", minHeight: 40, marginBottom: 10, borderRadius: 8, border: "none", padding: 8 }}
                  disabled={loading}
                />
                <div style={{ margin: "5px 0" }}>
                  <label>Rating: </label>
                  <select value={rating} onChange={e => setRating(Number(e.target.value))} disabled={loading}>
                    {[1,2,3,4,5].map(r => <option key={r} value={r}>{r} Star{r > 1 ? "s" : ""}</option>)}
                  </select>
                </div>
                <button className="neon-button" onClick={handleFeedback} disabled={loading || !message.trim()}>
                  Submit Feedback
                </button>
              </GlowCard>
            </animated.div>
          )
        )}

        {/* History Display */}
        <AnimatePresence>
          {history.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.6 }}
              className="history-container"
            >
              <div className="history-title">Your History</div>
              {history.map((item, idx) => (
                <motion.div
                  key={idx}
                  className="history-item"
                  initial={{ x: -100, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ duration: 0.5, delay: idx * 0.1 }}
                  whileHover={{
                    scale: 1.02,
                    boxShadow: "0 0 30px rgba(255, 0, 255, 0.5)"
                  }}
                >
                  <div>
                    <strong>Message:</strong> {item?.message || "No message"}
                  </div>
                  <div style={{ margin: '10px 0', fontSize: '1.5rem' }}>
                    <strong>Emojis:</strong> {renderEmojis(item?.emojis)}
                  </div>
                  <div>
                    <strong>Explanation:</strong> {item?.explanation || "No explanation"}
                  </div>
                  <div style={{ marginTop: '10px', color: '#888', fontSize: '0.9rem' }}>
                    <strong>Created:</strong> {item?.created_at || "Unknown"}
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error Display */}
        <AnimatePresence>
          {error && (
            <motion.div
              className="error-message"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.3 }}
            >
              <GlowCard
                borderColor="#ff4444"
                glowColor="rgba(255, 68, 68, 0.3)"
              >
                <div style={{ color: '#ff6b6b', textAlign: 'center' }}>
                  <strong>Error:</strong> {error}
                </div>
              </GlowCard>
            </motion.div>
          )}
        </AnimatePresence>
      </AppContainer>
    </animated.div>
  );
}

export default App;