import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import ListGroupItem from 'react-bootstrap/ListGroupItem';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      columns: 4,
      pools: {},
    };
    this.fetchData = this.fetchData.bind(this);
  }
  
  componentDidMount() {
    this.fetchData();
    this.setColumns();
    window.addEventListener('resize', this.setColumns.bind(this));
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.setColumns.bind(this));
  }

  setColumns() {
    if (window.innerWidth < 600) {
      this.setState({ columns: 1 });
    } else if (window.innerWidth < 900) {
      this.setState({ columns: 2 });
    } else if (window.innerWidth < 1200) {
      this.setState({ columns: 3 });
    } else {
      this.setState({ columns: 4 });
    }
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
      <Container fluid>
        <Row>
        {
          [...Array(this.state.columns).keys()].map(column =>(
            <Col key={column}>
              {
                Object.keys(this.state.pools).sort((pA, pB) => { return ((Object.keys(this.state.pools[pA]).length) < (Object.keys(this.state.pools[pB]).length)) ? -1 : ((Object.keys(this.state.pools[pA]).length) > (Object.keys(this.state.pools[pB]).length)) ? 1 : 0 }).filter((x, i) => ((i % this.state.columns === column) && (x !== 'count'))).map(project => (
                  <Card key={project}>
                    <Card.Header>
                        <strong>
                          {project}
                        </strong>
                        <small className="text-muted font-weight-light float-right">
                          {(Object.keys(this.state.pools[project]).length - 1)} active domain{((Object.keys(this.state.pools[project]).length - 1) === 1) ? '' : 's'},
                          &nbsp;{this.state.pools[project].count.instance} running instance{(this.state.pools[project].count.instance === 1) ? '' : 's'},
                          &nbsp;{this.state.pools[project].count.task}  recent task{(this.state.pools[project].count.task === 1) ? '' : 's'}
                        </small>
                    </Card.Header>
                    <ListGroup className="list-group-flush">
                      {
                        Object.keys(this.state.pools[project]).filter(x => x !== 'count').sort().map(domain => (
                          <ListGroupItem key={domain}>
                            <strong>
                              {domain}
                            </strong>
                            <small className="text-muted font-weight-light float-right">
                              {(Object.keys(this.state.pools[project][domain]).length - 1)} pool{((Object.keys(this.state.pools[project][domain]).length - 1) === 1) ? '' : 's'},
                              &nbsp;{this.state.pools[project][domain].count.instance} running instance{(this.state.pools[project][domain].count.instance === 1) ? '' : 's'},
                              &nbsp;{this.state.pools[project][domain].count.task}  recent task{(this.state.pools[project][domain].count.task === 1) ? '' : 's'}
                            </small>
                            <ul>
                              {
                                Object.keys(this.state.pools[project][domain]).filter(x => x !== 'count').sort().map(pool => (
                                  <li key={pool}>
                                    {pool}
                                    <small className="text-muted font-weight-light float-right">
                                      {this.state.pools[project][domain][pool].count.instance} running instance{(this.state.pools[project][domain][pool].count.instance === 1) ? '' : 's'},
                                      &nbsp;{this.state.pools[project][domain][pool].count.task}  recent task{(this.state.pools[project][domain][pool].count.task === 1) ? '' : 's'}
                                    </small>
                                  </li>
                                ))
                              }
                            </ul>
                          </ListGroupItem>
                        ))
                      }
                    </ListGroup>
                  </Card>
                ))
              }
            </Col>
          ))
        }
        </Row>
      </Container>
    );
  }
}

export default App;
