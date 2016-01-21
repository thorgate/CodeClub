

var Dashboard = React.createClass({

    getInitialState: function() {
        return {
            events: [],
            selectedEvent: null
        };
    },

    loadEvents: function() {
        $.ajax({
            url: EVENTS_URL,
            dataType: "json",
            cache: false,
            success: function (data) {
                data.unshift({
                    id: 0,
                    public: true,
                    title: "Overall"
                });

                var selectedEvent = data[0];
                var event_ids = data.map(function (event) {return event.id});
                if (this.state.selectedEvent != null && event_ids.indexOf(this.state.selectedEvent.id) >= 0) {
                    selectedEvent = this.state.selectedEvent;
                }

                this.setState({
                    events: data,
                    selectedEvent: selectedEvent
                });
            }.bind(this),
            error: function(xhr, status, err) {
                this.setState({
                    events: null,
                    selectedEvent: null
                });
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        })
    },

    componentDidMount: function() {
        this.loadEvents();
        setInterval(this.loadEvents, this.props.pollInterval)
    },

    changeSelectedEvent: function(event) {
        this.setState({selectedEvent: event});
    },

    render: function() {
        if (this.state.selectedEvent == null) {
            if (this.state.events == null) {
                return (
                    <div className="container">
                        <InfoMessage message="There was an error loading events" type="warning" />
                    </div>
                );
            }

            return null;
        }

        return (
            <div>
                <EventsMenu events={this.state.events} selectedEvent={this.state.selectedEvent.id} changeSelectedEvent={this.changeSelectedEvent} />
                <div className="container">
                    <h1>Leaderboard <small>{this.state.selectedEvent.title}</small></h1>
                    <Leaderboard pollInterval={15*1000} selectedEvent={this.state.selectedEvent}></Leaderboard>
                </div>
            </div>
        );
    }
});

var EventsMenu = React.createClass({
    render: function() {
        return (
            <div className="eventNav">
                <div className="container">
                    <ul>
                        {this.props.events.map(function(event) {
                            var selected = event.id == this.props.selectedEvent;
                            return <EventMenuItem key={event.id} event={event} selected={selected} changeSelectedEvent={this.props.changeSelectedEvent} />;
                        }.bind(this))}
                    </ul>
                </div>
            </div>
        );
    }
});

var EventMenuItem = React.createClass({

    handleClick: function(e) {
        e.preventDefault();

        this.props.changeSelectedEvent(this.props.event);
    },

    render: function() {
        var classString = this.props.selected ? "active " : "";

        if (!this.props.event.public) {
            classString += "warning "
        }

        return (
            <li><a href="#" className={classString} onClick={this.handleClick}>{ this.props.event.title }</a></li>
        );
    }
});

var Leaderboard = React.createClass({

    ongoingRequest: null,
    interval: null,
    selectedEvent: null,

    getInitialState: function() {
        return {
            contestants: "loading",

        };
    },

    loadContestants: function() {
        if (this.ongoingRequest) {
            this.ongoingRequest.abort();
        }

        var requestData = {};
        if (this.selectedEvent.id > 0) {
            requestData['event'] = this.selectedEvent.id;
        }

        this.ongoingRequest = $.ajax({
            url: CONTESTANTS_URL,
            dataType: "json",
            data: requestData,
            cache: false,
            success: function (data) {
                this.ongoingRequest = null;

                this.setState({contestants: data});
            }.bind(this),
            error: function(xhr, status, err) {
                this.ongoingRequest = null;

                this.setState({contestants: null});
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        })
    },

    componentDidMount: function() {
        if (this.interval) {
            clearInterval(this.interval);
        }
        this.selectedEvent = this.props.selectedEvent;
        this.loadContestants();
        this.interval = setInterval(this.loadContestants, this.props.pollInterval)
    },

    componentWillUnmount: function() {
        if (this.interval) {
            clearInterval(this.interval);
        }
    },

    componentWillReceiveProps: function(nextProps) {
        if (nextProps.selectedEvent == this.selectedEvent) {
            return;
        }
        if (this.interval) {
            clearInterval(this.interval);
        }
        this.setState({
            contestants: "loading"
        });
        this.selectedEvent = nextProps.selectedEvent;
        this.loadContestants();
        this.interval = setInterval(this.loadContestants, this.props.pollInterval)
    },

    render: function() {
        if (this.state.contestants == "loading") {
            return null
        }

        if (this.state.contestants == null) {
            return <InfoMessage message="There was an error loading contestants" type="warning" />
        }

        if (this.state.contestants.length == 0) {
            return <InfoMessage message="No correct solutions submitted yet" type="info" />
        }

        return (
            <div className="table-responsive">
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Contestant</th>
                            <th>Challenges</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.contestants.map(function(contestant, index) {
                            return <Contestant key={index} place={index+1} contestant={contestant} />;
                        })}
                    </tbody>
                </table>
            </div>
        );
    }
});

var Contestant = React.createClass({
    render: function() {
        return (
            <tr>
                <td>{this.props.place}</td>
                <td>{this.props.contestant.name}</td>
                <td>{this.props.contestant.challenges}</td>
                <td>{this.props.contestant.score}</td>
            </tr>
        );
    }
});

var InfoMessage = React.createClass({
    render: function() {
        return (
            <div className={"alert alert-" + this.props.type} role="alert">
                {this.props.message}
            </div>
        );
    }
});

ReactDOM.render(
  <Dashboard pollInterval={5*60*1000} />,
  document.getElementById('dashboard')
);
