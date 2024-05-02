import React from 'react';

const ElectoralVotesHeader = ({ demVotes, repVotes, threshold }) => {
  const totalVotes = demVotes + repVotes;
  const demPercentage = (demVotes / totalVotes) * 100;
  const repPercentage = (repVotes / totalVotes) * 100;

  // Determine the winner based on the threshold
  var winner = ''
  if ((demVotes >= threshold) && (repVotes >= threshold))  {
    if (demVotes > repVotes) {
        winner = 'Democrats';
    } else if (repVotes > demVotes) {
        winner = 'Republicans';
    } else {
        winner = 'Undetermined';
    }
  } else if (demVotes >= threshold) {
    winner = 'Democrats';
  } else if (repVotes >= threshold) {
    winner = 'Republicans';
  } else {
    winner = 'Undetermined';
  }

  return (
    <div style={{ marginBottom: '20px' }}>
      <h1 style={{ textAlign: 'center' }}>{winner ? `${winner} take the Presidency` : 'House Results'}</h1>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ color: `#0066cb` }}>Dem {demVotes}</span>
        <div style={{ flexGrow: 1, height: '20px', backgroundColor: '#ddd', margin: '0 20px', position: 'relative' }}>
          <div style={{ width: `${demPercentage}%`, height: '100%', backgroundColor: `#0066cb`, position: 'absolute', left: 0, top: 0 }}></div>
          <div style={{ width: `${repPercentage}%`, height: '100%', backgroundColor: `#ec3a38`, position: 'absolute', left: `${demPercentage}%`, top: 0 }}></div>
            <div style={{ position: 'absolute', left: '50%', top: '-10px', marginLeft: '-1px', width: '2px', height: '40px', backgroundColor: 'black' }}></div>
        </div>
        <span style={{ color: `#ec3a38` }}>Rep {repVotes}</span>
      </div>
      <div style={{ textAlign: 'center', marginTop: '10px'}}>{threshold} to win</div>
    </div>
  );
};

export default ElectoralVotesHeader;