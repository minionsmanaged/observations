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
      projects: [
        'gecko'
      ],
      domains: [
        'gecko-1',
        'gecko-3',
        'gecko-t'
      ],
      workers: [
        'b-linux',
        'b-linux-aws',
        'b-linux-xlarge',
        'b-win2012',
        't-win10-64',
        't-win10-64-gpu-s',
        't-win7-32',
        't-win7-32-gpu',
        't-linux-large',
        't-linux-xlarge'
      ],
      columns: 4,
      fluid: false,
      pools: {}
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
    if ((Object.keys(this.state.pools).length < 3) || (window.innerWidth < 600)) {
      this.setState({ columns: 1, fluid: false });
    } else if (window.innerWidth < 900) {
      this.setState({ columns: 2, fluid: false });
    } else if (window.innerWidth < 1200) {
      this.setState({ columns: 3, fluid: true });
    } else {
      this.setState({ columns: 4, fluid: true });
    }
  }
  
  fetchData() {
    fetch('https://raw.githubusercontent.com/minionsmanaged/observations/master/pools.json')
      .then(response => response.json())
      .then(pools => {
        this.setState(state => {
          // filter by state.projects
          state.pools = (state.projects === undefined || state.projects.length === 0)
            ? pools
            : state.projects.reduce((o, k) => ({ ...o, [k]: pools[k] }), {});
          return state;
        });
      });
  }

  render() {
    return (
      <Container fluid={this.state.fluid}>
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
                        Object.keys(this.state.pools[project]).filter(x => ((x !== 'count') && ((this.state.domains === undefined || this.state.domains.length === 0) || this.state.domains.includes(x)))).sort().map(domain => (
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
                                Object.keys(this.state.pools[project][domain]).filter(x => ((x !== 'count') && ((this.state.workers === undefined || this.state.workers.length === 0) || this.state.workers.includes(x)))).sort().map(pool => (
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
