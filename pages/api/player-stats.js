import { openDb } from '../../lib/db'

export default async function handler(req, res) {
  const { player } = req.query;
  console.log('Received request for player:', player);
  
  try {
    const db = await openDb();
    console.log('Database opened successfully');
    
    const query = `SELECT Season as year, PTS as ppg
                   FROM bball_ref_players_1998_2023
                   WHERE Player LIKE ?
                   ORDER BY Season ASC`;
    console.log('Executing query:', query);
    
    const playerStats = await db.all(query, [`%${player}%`]);
    console.log('Query results:', playerStats);

    const stats = playerStats.map(stat => ({
      year: stat.year,
      ppg: parseFloat(stat.ppg)
    }));

    res.status(200).json(stats);
  } catch (error) {
    console.error('Error fetching player stats:', error);
    res.status(500).json({ error: 'Error fetching player stats', details: error.message });
  }
}