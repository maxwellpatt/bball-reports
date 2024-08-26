import { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function Home() {
  const [player, setPlayer] = useState('');
  const [stats, setStats] = useState([]);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.get(`/api/player-stats?player=${player}`);
      setStats(response.data);
      if (response.data.length === 0) {
        setError('No stats found for this player.');
      }
    } catch (error) {
      console.error('Error fetching player stats:', error);
      setError('Error fetching player stats. Please try again.');
    }
  };

  const chartData = {
    labels: stats.map(stat => stat.year),
    datasets: [
      {
        label: 'Points Per Game',
        data: stats.map(stat => stat.ppg),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${player}'s Points Per Game Over Seasons`,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Points Per Game'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Season'
        }
      }
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Basketball Player Stats</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <input
          type="text"
          value={player}
          onChange={(e) => setPlayer(e.target.value)}
          placeholder="Enter player name"
          className="border p-2 mr-2"
        />
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">
          Get Stats
        </button>
      </form>
      {error && <p className="text-red-500">{error}</p>}
      {stats.length > 0 && (
        <div className="mt-4">
          <Line data={chartData} options={chartOptions} />
        </div>
      )}
    </div>
  );
}