import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import ListGroupItem from 'react-bootstrap/ListGroupItem';
import Form from 'react-bootstrap/Form';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      filter: {
        option: {
          projects: [],
          domains: [],
          workers: []
        },
        selection: {
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
          ]
        }
      },
      columns: 4,
      fluid: false,
      pools: {}
    };
    this.fetchData = this.fetchData.bind(this);
    //this.handleFilterChange = this.handleFilterChange.bind(this);
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
          // filter by state.filter.selection.projects
          state.pools = (state.filter.selection.projects === undefined || state.filter.selection.projects.length === 0)
            ? pools
            : state.filter.selection.projects.reduce((o, k) => ({ ...o, [k]: pools[k] }), {});

          // populate filter options
          state.filter.option.projects = Object.keys(pools).filter(x => x !== 'count').sort();
          state.filter.option.projects.forEach(project => {
            state.filter.option.domains = [...new Set([...state.filter.option.domains, ...Object.keys(pools[project]).filter(x => x !== 'count')])].sort();
            Object.keys(pools[project]).forEach(domain => {
              state.filter.option.workers = [...new Set([...state.filter.option.workers, ...Object.keys(pools[project][domain]).filter(x => x !== 'count')])].sort();
            });
          });
          return state;
        });
      });
  }

  /*
  handleFilterChange(event) {
    let id = event.target.id.split('_');
    let filter = id[1];
    let property = id[2];
    this.setState(state => {
      let index = state.filter.selection[filter].indexOf(property);
      if (index > -1) {
        state.filter.selection[filter].splice(index, 1);
      } else {
        state.filter.selection[filter].push(property);
      }
      return state;
    });
  }
  */

  render() {
    return (
      <Container fluid={this.state.fluid}>
        <Row>
          <Col>
            {
              ['projects', 'domains', 'workers'].map(filter => (
                <div>
                  <h6>{filter}</h6>
                  {
                    this.state.filter.option[filter].map(property => (
                      <Form.Check
                        type="checkbox"
                        onChange={()=>{}/*this.handleFilterChange*/}
                        checked={this.state.filter.selection[filter].includes(property)}
                        label={property}
                        id={'filter_' + filter + '_' + property}
                        key={'filter_' + filter + '_' + property} />
                    ))
                  }
                </div>
              ))
            }
          </Col>
        {
          [...Array(this.state.columns).keys()].map(column =>(
            <Col key={column} xs={10}>
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
