import React, { useState, useEffect  } from 'react';
import USAMap from "react-usa-map";
import './ElectionMap.css';
import ElectionHeader from './ElectionHeader';

const demVotes = 232;
const repVotes = 198;
const threshold = 218;

const dem_results = {
    'ALABAMA': 0.38029734886419575, 
    'ALASKA': 0.3361422547830829, 
    'ARIZONA': 0.3528904451664854, 
    'ARKANSAS': 0.42153975759458256, 
    'CALIFORNIA': 0.4780004050359183, 
    'COLORADO': 0.4101641978503422, 
    'CONNECTICUT': 0.46311521662332655, 
    'DELAWARE': 0.49380526970808486, 
    'DISTRICT OF COLUMBIA': 0.8563579638459574, 
    'FLORIDA': 0.41649828841557124, 
    'GEORGIA': 0.4377849405431513, 
    'HAWAII': 0.39608875942778965, 
    'IDAHO': 0.29827977854966103, 
    'ILLINOIS': 0.48339141460175006, 
    'INDIANA': 0.398799733109181, 
    'IOWA': 0.4720828575296582, 
    'KANSAS': 0.3665306765274193, 
    'KENTUCKY': 0.3884951800038314, 
    'LOUISIANA': 0.42355236196824503, 
    'MAINE': 0.4750614874845557, 
    'MARYLAND': 0.5076399440393307, 
    'MASSACHUSETTS': 0.4914446939553423, 
    'MICHIGAN': 0.4821185553296514, 
    'MINNESOTA': 0.49173365574042704, 
    'MISSISSIPPI': 0.41395052828014894, 
    'MISSOURI': 0.44245568346068226, 
    'MONTANA': 0.37740697179964583, 
    'NEBRASKA': 0.34267711668575407, 
    'NEVADA': 0.37667522869250747, 
    'NEW HAMPSHIRE': 0.4027616319433327, 
    'NEW JERSEY': 0.45118512214272366, 
    'NEW MEXICO': 0.38651704331723125, 
    'NEW YORK': 0.4486969490913547, 
    'NORTH CAROLINA': 0.44032170992502406, 
    'NORTH DAKOTA': 0.3408021055479763, 
    'OHIO': 0.44694821483414643, 
    'OKLAHOMA': 0.3438475858271592, 
    'OREGON': 0.4794913772936301, 
    'PENNSYLVANIA': 0.4574988460053556, 
    'RHODE ISLAND': 0.5397197104792263, 
    'SOUTH CAROLINA': 0.40216437156692286, 
    'SOUTH DAKOTA': 0.38526307172151486, 
    'TENNESSEE': 0.4299633810263514, 
    'TEXAS': 0.3963983320575276, 
    'UTAH': 0.28978525186231197, 
    'VERMONT': 0.50738010604225, 
    'VIRGINIA': 0.4278461717904831, 
    'WASHINGTON': 0.47759292687395793, 
    'WEST VIRGINIA': 0.4201891510252027, 
    'WISCONSIN': 0.47889167634397733, 
    'WYOMING': 0.30559872978296476
}

const rep_results = {
    'ALABAMA': 0.5919047649721833, 
    'ALASKA': 0.5616439699389687, 
    'ARIZONA': 0.5273339268982333, 
    'ARKANSAS': 0.5372467865808758, 
    'CALIFORNIA': 0.4098858435618017, 
    'COLORADO': 0.5089875287622793, 
    'CONNECTICUT': 0.4100408140426839, 
    'DELAWARE': 0.4552661055271963, 
    'DISTRICT OF COLUMBIA': 0.09910197122901462, 
    'FLORIDA': 0.5167712443451875, 
    'GEORGIA': 0.5325500714018071, 
    'HAWAII': 0.49260303575214903, 
    'IDAHO': 0.6202098295459102, 
    'ILLINOIS': 0.4635298978048178, 
    'INDIANA': 0.5550582170519708, 
    'IOWA': 0.46609898765986846, 
    'KANSAS': 0.561073288588235, 
    'KENTUCKY': 0.5719261710909255, 
    'LOUISIANA': 0.5416743558220387, 
    'MAINE': 0.47866010020256555, 
    'MARYLAND': 0.41566241812608345, 
    'MASSACHUSETTS': 0.3398114951668002, 
    'MICHIGAN': 0.4708947846442653, 
    'MINNESOTA': 0.43881920191916685, 
    'MISSISSIPPI': 0.5613610133769005, 
    'MISSOURI': 0.511115159168689, 
    'MONTANA': 0.5594447055550544, 
    'NEBRASKA': 0.5687573903439702, 
    'NEVADA': 0.5155441452039528, 
    'NEW HAMPSHIRE': 0.4993626982990872, 
    'NEW JERSEY': 0.46638865210861136, 
    'NEW MEXICO': 0.5246613654599703, 
    'NEW YORK': 0.37189465960348456, 
    'NORTH CAROLINA': 0.5294125961517281, 
    'NORTH DAKOTA': 0.5859991827011516, 
    'OHIO': 0.5028357622968086, 
    'OKLAHOMA': 0.6060983196139881, 
    'OREGON': 0.4425880485591121, 
    'PENNSYLVANIA': 0.47344527219187266, 
    'RHODE ISLAND': 0.3638871176360601, 
    'SOUTH CAROLINA': 0.5683670606582065, 
    'SOUTH DAKOTA': 0.5564503971639729, 
    'TENNESSEE': 0.5412508496995988, 
    'TEXAS': 0.521966165772772, 
    'UTAH': 0.5817418250674404, 
    'VERMONT': 0.40452333634142335, 
    'VIRGINIA': 0.5146076913106581, 
    'WASHINGTON': 0.44558887469929165, 
    'WEST VIRGINIA': 0.5465503835322882, 
    'WISCONSIN': 0.46411373593932304, 
    'WYOMING': 0.620330312032094
}

const stateAbbreviations = {
    'ALABAMA': 'AL',
    'ALASKA': 'AK',
    'ARIZONA': 'AZ',
    'ARKANSAS': 'AR',
    'CALIFORNIA': 'CA',
    'COLORADO': 'CO',
    'CONNECTICUT': 'CT',
    'DELAWARE': 'DE',
    'DISTRICT OF COLUMBIA': 'DC',
    'FLORIDA': 'FL',
    'GEORGIA': 'GA',
    'HAWAII': 'HI',
    'IDAHO': 'ID',
    'ILLINOIS': 'IL',
    'INDIANA': 'IN',
    'IOWA': 'IA',
    'KANSAS': 'KS',
    'KENTUCKY': 'KY',
    'LOUISIANA': 'LA',
    'MAINE': 'ME',
    'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA',
    'MICHIGAN': 'MI',
    'MINNESOTA': 'MN',
    'MISSISSIPPI': 'MS',
    'MISSOURI': 'MO',
    'MONTANA': 'MT',
    'NEBRASKA': 'NE',
    'NEVADA': 'NV',
    'NEW HAMPSHIRE': 'NH',
    'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM',
    'NEW YORK': 'NY',
    'NORTH CAROLINA': 'NC',
    'NORTH DAKOTA': 'ND',
    'OHIO': 'OH',
    'OKLAHOMA': 'OK',
    'OREGON': 'OR',
    'PENNSYLVANIA': 'PA',
    'RHODE ISLAND': 'RI',
    'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD',
    'TENNESSEE': 'TN',
    'TEXAS': 'TX',
    'UTAH': 'UT',
    'VERMONT': 'VT',
    'VIRGINIA': 'VA',
    'WASHINGTON': 'WA',
    'WEST VIRGINIA': 'WV',
    'WISCONSIN': 'WI',
    'WYOMING': 'WY'
}; 
const abbreviationsToStates = Object.fromEntries(
  Object.entries(stateAbbreviations).map(([state, abbr]) => [abbr, state])
);

function toTitleCase(str) {
  return str.toLowerCase().replace(/\b\w/g, function(char) {
    return char.toUpperCase();
  });
}
     
const getPartyColor = (dem_percentage, rep_percentage) => {
    //const hue = percentage * 450; // 0% is red, 100% is blue
    if (dem_percentage > rep_percentage) {
        return `#0066cb`;
    } else {
        return `#ec3a38`;
    }
  };
  
  const ElectionMap = () => {
    const [votes, setVotes] = useState({ democratic: 0, republican: 0, threshold: 0});
    const [dem, setDem] = useState({democratic: 0, republican: 0, threshold: 0});
    const [rep, setRep] = useState({democratic: 0, republican: 0, threshold: 0});
    const [stateData, setStateData] = useState({});
    const [year, setYear] = useState(2020);

    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

    useEffect(() => {
      // Function to update the state with the new mouse position
      const updateMousePosition = (event) => {
        setMousePosition({ x: event.pageX, y: event.pageY });
      };

      // Adding the event listener when the component mounts
      window.addEventListener('click', updateMousePosition);

      // Cleanup function to remove the event listener when the component unmounts
      return () => {
        window.removeEventListener('click', updateMousePosition);
      };
    }, []);

    const fetchVotes = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/votes');
        const data = await response.json();
        console.log(data)
        setVotes({ democratic: data.democratic, republican: data.republican, threshold: data.threshold});
      } catch (error) {
        console.error("Failed to fetch votes:", error);
      }
    };

    const fetchVotes2024 = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/votes2024');
        const data = await response.json();
        console.log(data)
        setVotes({ democratic: data.democratic, republican: data.republican, threshold: data.threshold});
      } catch (error) {
        console.error("Failed to fetch votes:", error);
      }
    };

    useEffect(() => {
      // Fetch the votes from the Python backend
      fetchVotes();
    }, []);

    const fetchDemResults = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/democratic');
        const data = await response.json();
        console.log(data)
        setDem(data);
      } catch (error) {
        console.error("Failed to fetch democratic results:", error);
      }
    };

    useEffect(() => {
      // Fetch the votes from the Python backend
      fetchDemResults();
    }, []);

    // Fetch the votes from the Python backend
      const fetchDemResults2024 = async () => {
        try {
          const response = await fetch('http://127.0.0.1:5000/democratic2024');
          const data = await response.json();
          console.log(data)
          setDem(data);
        } catch (error) {
          console.error("Failed to fetch democratic results:", error);
        }
      };

      const fetchRepResults = async () => {
        try {
          // FIX TO BE REPUBLICAN RESULTS!!!
          const response = await fetch('http://127.0.0.1:5000/republican');
          const data = await response.json();
          console.log(data)
          setRep(data);
        } catch (error) {
          console.error("Failed to fetch republican results:", error);
        }
      };


    useEffect(() => {
      // Fetch the votes from the Python backend

      fetchRepResults();
    }, []);


    // Fetch the votes from the Python backend
    const fetchRepResults2024 = async () => {
      try {
        // FIX TO BE REPUBLICAN RESULTS!!!
        const response = await fetch('http://127.0.0.1:5000/republican2024');
        const data = await response.json();
        console.log(data)
        setRep(data);
      } catch (error) {
        console.error("Failed to fetch republican results:", error);
      }
    };

    
    // THIS IS A BIG ISSUE! The function is returning an error
    // But the code is correct: it is actually returning a dictionary
    useEffect(() => {
      if (Object.keys(dem).length && Object.keys(rep).length) {  // Ensure both results are fetched
        const newData = Object.keys(dem).reduce((obj, state) => {
          const dem_percentage = dem[state];
          const rep_percentage = rep[state];
          if (state in stateAbbreviations) { // Check if state abbreviation exists
            obj[stateAbbreviations[state]] = {
              color: getPartyColor(dem_percentage, rep_percentage),
              democrat: Math.round(dem_percentage * 100),
              republican: Math.round(rep_percentage * 100)
            };
          }
          return obj;
        }, {});
        setStateData(newData);
      }
    }, [dem, rep]);  // Dependency array to trigger re-calculation
    
    const [infoBox, setInfoBox] = useState({ visible: false, content: {} });
    const [hover, setHover] = useState(false);  // State to manage hover effect
  
    // Handle the click on a state
    const mapHandler = (event) => {
      const stateAbbr = event.target.dataset.name;
      const data = stateData[stateAbbr];

      if (stateData[stateAbbr]) {
        setInfoBox({
          visible: true,
          content: {
            name: toTitleCase(abbreviationsToStates[stateAbbr]),
            democrat: stateData[stateAbbr].democrat,
            republican: stateData[stateAbbr].republican
          }
        });
      }
    };

    // Function to handle mouse entering a state
    const handleMouseEnter = (event) => {
        const stateAbbr = event.target.dataset.name;
        const data = stateData[stateAbbr];
        if (stateData[stateAbbr]) {
            setInfoBox({
                visible: true,
                content: {
                name: stateAbbr,
                democrat: stateData[stateAbbr].democrat,
                republican: stateData[stateAbbr].republican
                }
            });
        }
    };

    const handleMouseLeave = () => {
        setInfoBox({ visible: false, content: {} });
    };
  
    // Customizing the states' colors based on the data
    const statesCustomConfig = () => {
      return Object.keys(stateData).reduce((config, stateKey) => {
        config[stateKey] = {
            fill: stateData[stateKey].color,
            clickHandler: () => mapHandler({ target: { dataset: { name: stateKey } } }),
            onMouseOver: (e) => handleMouseEnter({ target: { dataset: { name: stateKey } } }),
            onMouseOut: (e) => handleMouseLeave
        };
        return config;
      }, {});
    };
  
    
    const fetchAllResults2020 = () => {
      fetchDemResults();
      fetchRepResults();
      fetchVotes();
      setYear("2020");
    };

    const fetchAllResults2024 = () => {
      fetchDemResults2024();
      fetchRepResults2024();
      fetchVotes2024();
      setYear("2024");
    };

    function NavigationBar() {
      // Function handlers would be defined or passed into this component
    
      return (
        <div style={{
          position: 'relative',
          width: '100%',
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'space-around',
          alignItems: 'center',
          backgroundColor: '#333',  // Dark grey, which is more professional
          color: 'white',            // Ensure text is easily readable
          padding: '10px 0',         // Vertical padding for better aesthetics
          boxShadow: '0 2px 5px rgba(0,0,0,0.2)'  // Subtle shadow for depth
        }}>
          <h2 style={{
            margin: 0,                // Removes default margin
            padding: '0 20px',        // Padding on the sides for space around text
            fontWeight: 'normal',     // Optional: adjusts weight of the font
            fontSize: '20px',         // Larger text for the heading
          }}>
            CDS Datathon 2024
          </h2>
          <h2 style={{
            margin: 0,                // Removes default margin
            paddingRight: 60,         // Padding on the sides for space around text
            fontWeight: 'normal',     // Optional: adjusts weight of the font
            fontSize: '24px',         // Larger text for the heading
          }}>
            Results for {year}
          </h2>
          <div style={{
            textAlign: 'center',
          }}>
            <button 
              onClick={fetchAllResults2020}
              style={{
                backgroundColor: '#007BFF', // Bootstrap's primary button color
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                padding: '10px 15px',
                cursor: 'pointer',
                fontSize: '16px',
                transition: 'background-color 0.3s'
              }}
              onMouseOver={(e) => e.target.style.backgroundColor = '#0056b3'}
              onMouseOut={(e) => e.target.style.backgroundColor = '#007BFF'}
            >
              2020
            </button>
            <button 
              onClick={fetchAllResults2024}
              style={{
                backgroundColor: '#28A745', // Green, visually distinct from the first button
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                padding: '10px 15px',
                marginLeft: '10px',
                cursor: 'pointer',
                fontSize: '16px',
                transition: 'background-color 0.3s'
              }}
              onMouseOver={(e) => e.target.style.backgroundColor = '#19692c'}
              onMouseOut={(e) => e.target.style.backgroundColor = '#28A745'}
            >
              2024
            </button>
          </div>
        </div>
      );
    }

    return (
      <div style={{ position: 'relative', 
        width: '100%', 
        height: '100vh', 
        display: 'flex', 
        flexDirection: 'column',
        justifyContent: 'center', 
        alignItems: 'center'}}>
      <NavigationBar></NavigationBar>
      <ElectionHeader demVotes={votes.democratic} repVotes={votes.republican} threshold={votes.threshold} />

      <USAMap customize={statesCustomConfig()}/>

      <div style={{ marginBottom: '30px' }}>
        <h2></h2>
      </div>
      
      {infoBox.visible && (
      <div style={{
        position: 'absolute',
        top: `${mousePosition.y}px`,
        left: `${mousePosition.x}px`,
        transform: 'translate(-50%, -50%)',
        backgroundColor: 'white',
        padding: '20px',
        border: '1px solid #ccc',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        borderRadius: '8px',
        zIndex: 10,
        width: 'fit-content',
        maxWidth: '90%',
        overflow: 'hidden'
      }}
      onMouseEnter={() => setHover(true)}  // Set hover state to true
      onMouseLeave={() => setHover(false)}  // Set hover state to false
      >
      <h3 style={{
        fontSize: '20px',  // Larger font size for the header
        borderBottom: '1px solid #eee',  // Subtle line under the header
        paddingBottom: '10px',  // Padding under the header
        marginBottom: '10px'  // Margin to separate header from content
      }}>{infoBox.content.name}</h3>
      <p style={{ margin: '5px 0' }}>Democrat: {infoBox.content.democrat}%</p>
      <p style={{ margin: '5px 0' }}>Republican: {infoBox.content.republican}%</p>
      <button onClick={() => setInfoBox({ visible: false, content: {} })}
        style={{
          backgroundColor: '#28A745',  // Consistent button color
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          padding: '8px 16px',
          cursor: 'pointer',
          fontSize: '16px',
          transition: 'background-color 0.3s',
          marginTop: '10px'  // Space above the button
        }}
        onMouseOver={(e) => e.target.style.backgroundColor = '#19692c'}
        onMouseOut={(e) => e.target.style.backgroundColor = '#28A745'}
        >
        Close
          </button>
        </div>
      )}
    </div>
    );
  };
  
  export default ElectionMap;