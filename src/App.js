import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      pools: {}
    };
    this.fetchData = this.fetchData.bind(this);
  }
  
  componentDidMount() {
    this.fetchData();
  }
  
  fetchData() {
    fetch('https://raw.githubusercontent.com/minionsmanaged/observations/master/pools.json')
      .then(response => response.json())
      .then(pools => {
        this.setState(state => {
          state.pools = pools;
          return state;
        });
      });
  }

  render() {
    return (
      <Container>
        {
          Object.keys(this.state.pools).filter(x => x !== 'count').sort().map(project => (
            <Row key={project}>
              <div>
                <h3>{project}</h3>
                {
                  Object.keys(this.state.pools[project]).filter(x => x !== 'count').sort().map(domain => (
                    <div key={domain}>
                      <h4>{domain}</h4>
                      {
                        Object.keys(this.state.pools[project][domain]).filter(x => x !== 'count').sort().map(pool => (
                          <div key={pool}>
                            <h5>{pool}</h5>
                          </div>
                        ))
                      }
                    </div>
                  ))
                }
              </div>
              <hr />
            </Row>
          ))
        }
      </Container>
    );
  }
}

export default App;
