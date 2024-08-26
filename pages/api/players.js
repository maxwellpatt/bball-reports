import { openDb } from '../../lib/db'

export default async function handler(req, res) {
  try {
    const db = await openDb();
    const players = await db.all(`
      SELECT * FROM fantrax_8_25_24
      ORDER BY fantasy_team, rkov
    `);

    const groupedPlayers = players.reduce((acc, player) => {
      if (!acc[player.fantasy_team]) {
        acc[player.fantasy_team] = [];
      }
      acc[player.fantasy_team].push(player);
      return acc;
    }, {});

    res.status(200).json(groupedPlayers);
  } catch (error) {
    console.error('Error fetching players:', error);
    res.status(500).json({ error: 'Error fetching players' });
  }
}