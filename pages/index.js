import { useState, useEffect } from 'react';
import axios from 'axios';
import PlayerCard from '../components/PlayerCard';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [teams, setTeams] = useState({});

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await axios.get('/api/players');
        const filteredTeams = Object.fromEntries(
          Object.entries(response.data).filter(([teamName]) => teamName !== 'FA')
        );
        setTeams(filteredTeams);
      } catch (error) {
        console.error('Error fetching players:', error);
      }
    };

    fetchPlayers();
  }, []);

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Fantasy Basketball Teams</h1>
      <div className={styles.teamsContainer}>
        {Object.entries(teams).map(([teamName, players]) => (
          <div key={teamName} className={styles.team}>
            <h2 className={styles.teamName}>{teamName}</h2>
            <div className={styles.playersGrid}>
              {players.map(player => (
                <PlayerCard key={player.id} player={player} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}