import React from 'react';
import { Tooltip } from 'react-tooltip';
import styles from '../styles/PlayerCard.module.css';

const PlayerCard = ({ player }) => {
  return (
    <div 
      className={styles.playerCard}
      data-tooltip-id={`tooltip-${player.id}`}
    >
      <p className={styles.playerName}>{player.player}</p>
      <Tooltip id={`tooltip-${player.id}`} className={styles.tooltip}>
        <div className={styles.tooltipContent}>
          <p><strong>Age:</strong> {player.age}</p>
          <p><strong>Position:</strong> {player.position}</p>
          <p><strong>FP/G:</strong> {player.fp_per_g.toFixed(1)}</p>
          <p><strong>PTS:</strong> {player.pts.toFixed(1)}</p>
          <p><strong>REB:</strong> {player.reb.toFixed(1)}</p>
          <p><strong>AST:</strong> {player.ast.toFixed(1)}</p>
          <p><strong>STL:</strong> {player.st.toFixed(1)}</p>
          <p><strong>BLK:</strong> {player.blk.toFixed(1)}</p>
          <p><strong>3PTM:</strong> {player['3ptm'].toFixed(1)}</p>
        </div>
      </Tooltip>
    </div>
  );
};

export default PlayerCard;