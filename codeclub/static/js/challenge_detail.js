

var ChallengeDetail = React.createClass({

    getInitialState: function() {
        return {
            challenge: "loading",
            solutions: [],
            correct_users: []
        };
    },

    loadChallenge: function() {
        $.ajax({
            url: this.props.url,
            dataType: "json",
            cache: false,
            success: function (data) {
                this.setState({
                    challenge: data.challenge,
                    solutions: data.solutions,
                    correct_users: data.correct_users
                });
            }.bind(this),
            error: function(xhr, status, err) {
                this.setState({challenge: null, solutions: [], correct_users: []});
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        })
    },

    componentDidMount: function() {
        this.loadChallenge();
        setInterval(this.loadChallenge, this.props.pollInterval)
    },

    render: function() {
        if (this.state.challenge == "loading") {
            return null
        }

        if (this.state.challenge == null) {
            return (
                <div className="alert alert-warning" role="alert">
                    Couldn't load the challenge with your solutions
                </div>
            );
        }

        var non_public_warning = null;
        if (!this.state.challenge.public) {
            non_public_warning = (
                <div className="alert alert-warning" role="alert">
                    Challenge is not public
                </div>
            );
        }

        return (
            <div>
                <div className="jumbotron">
                    <h1>{ this.state.challenge.title } <small>by { this.state.challenge.author }</small></h1>
                    {non_public_warning}
                    <div dangerouslySetInnerHTML={{ __html: marked(this.state.challenge.description, {sanitize: true}) }}></div>
                </div>

                <div className="row">
                    <div className="col-xs-12 col-md-push-6 col-md-6">
                        <UserList users={this.state.correct_users} />
                    </div>
                    <div className="col-xs-12 col-md-pull-6 col-md-6">
                        <h2>Your solutions</h2>
                        <SolutionList solutions={this.state.solutions} />
                    </div>
                </div>
            </div>
        );
    }
});

var UserList = React.createClass({
    render: function() {
        if (this.props.users.length == 0) {
            return <h2>No correct solutions yet :(</h2>
        }

        return (
            <div>
                <h2>Correct solutions from:</h2>
                { this.props.users.join(", ") }
            </div>
        );
    }
});

var SolutionList = React.createClass({
    render: function() {
        if (this.props.solutions.length == 0) {
            return <div className="alert alert-info">You don't have any submitted solutions :(</div>
        }

        return (
            <div>
                <div className="list-group">
                    {this.props.solutions.map(function(solution, index) {
                        return <Solution key={index} solution={solution} />;
                    }.bind(this))}
                </div>
            </div>
        );
    }
});

var Solution = React.createClass({
    render: function() {
        var labelClass = "label solution-info-label";
        labelClass += " label-" + (this.props.solution.bootstrap_class || "default");

        return (
            <a href={ this.props.solution.url } className="list-group-item">
                <span className="pull-right">
                    { this.props.solution.timestamp }
                </span>

                <span className={labelClass}>{ this.props.solution.status_title}</span>
                { this.props.solution.filename }
            </a>
        );
    }
});

ReactDOM.render(
    <ChallengeDetail pollInterval={5*1000} url={CHALLENGE_URL} />,
    document.getElementById('challenge_detail')
);