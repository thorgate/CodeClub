

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

        var golf_label = null;
        if (this.state.challenge.golf) {
            golf_label = (
                <span className="label label-default">GOLF</span>
            );
        }

        return (
            <div>
                <div className="jumbotron">
                    <h1>{ this.state.challenge.title } <small>by { this.state.challenge.author }</small></h1>
                    <p>
                        <span className="label label-primary">{this.state.challenge.calculated_points}</span>
                        {golf_label}
                        {non_public_warning}
                    </p>
                    <div dangerouslySetInnerHTML={{ __html: marked(this.state.challenge.description, {sanitize: true}) }}></div>
                </div>

                <div className="row">
                    <div className="col-xs-12 col-md-push-6 col-md-6">
                        <UserList
                            users={this.state.correct_users}
                            golf={this.state.challenge.golf}
                            points={this.state.challenge.calculated_points}
                        />
                    </div>
                    <div className="col-xs-12 col-md-pull-6 col-md-6">
                        <h2>Your solutions</h2>
                        <SolutionList solutions={this.state.solutions} golf={this.state.challenge.golf}/>
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

        function getGolfPoints(challengePoints, minBytes, userBytes) {
            return Math.floor((minBytes / userBytes) * challengePoints);
        }

        var displayedUsers = this.props.users.map(function(user, index) {
            if (!this.props.golf)
                return (
                    <tr key={index}>
                        <td>{index + 1}</td>
                        <td>{user.name}</td>
                    </tr>
                );
            return (
                <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{user.name}</td>
                    <td>{user.solution_size}</td>
                    <td>{getGolfPoints(this.props.points, this.props.users[0].solution_size, user.solution_size)}</td>
                </tr>
            );
        }.bind(this));

        return (
            <div>
                <h2>Correct solutions from:</h2>
                <div className="user-list">
                    <table className="table table-striped table-hover">
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            {this.props.golf ? <th>Bytes</th> : null}
                            {this.props.golf ? <th>Points</th> : null}
                        </tr>
                        </thead>
                        <tbody>
                            {displayedUsers}
                        </tbody>
                    </table>
                </div>
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
                        return <Solution key={index} solution={solution} golf={this.props.golf}/>;
                    }.bind(this))}
                </div>
            </div>
        );
    }
});

var Feedback = React.createClass({
    render: function() {
        return (
            <span>
                { this.props.tests.map(
                    function (test, index) {
                        var label = 'success';
                        if (test.flavor === 'FAIL') {
                            label = 'danger';
                        } else if (test.flavor === 'ERROR') {
                            label = 'warning';
                        }
                        var time = Math.round(test.seconds * 100) / 100;
                        return (
                            <span key={index} className="list-group-item tests">
                                <span className={"label solution-info-label label-"+label}>{test.flavor}</span>
                                {test.test}
                                <span className={"label label-default pull-right"}>{time} sec</span>
                            </span>
                        );
                    }
                )}
            </span>
        );
    }
});

var Solution = React.createClass({
    render: function() {
        var labelClass = "label solution-info-label";
        labelClass += " label-" + (this.props.solution.bootstrap_class || "default");

        var sizeBlock = this.props.golf ? this.props.solution.filesize + " bytes" : null;
        var fileName = this.props.solution.filename;
        var cutFileName = (fileName.length > 15) ? fileName.substr(0,15-1)+'...' : fileName;
        var target = "summary" + this.props.solution.id;
        var feedback = null;
        if (this.props.solution.TODO.tests) {
            feedback = (<div id={ target } className="collapse">
                <Feedback tests={this.props.solution.TODO.tests }/>
            </div>);
        }

        return (
            <span>
                <div
                    className="list-group-item"
                    data-toggle="collapse"
                    data-target={ '#' + target }
                >
                    <span className="pull-right">{ this.props.solution.timestamp }</span>

                    <span className={labelClass} title={ this.props.solution.id }>{ this.props.solution.status_title}</span>

                    <span className="label solution-info-label label-default">
                        { sizeBlock }
                    </span>
                    <a className="label solution-info-label label-default" href={ this.props.solution.url }>
                        { cutFileName }
                    </a>

                </div>
                { feedback }

            </span>
        );
    }
});

ReactDOM.render(
    <ChallengeDetail pollInterval={5*1000} url={CHALLENGE_URL} />,
    document.getElementById('challenge_detail')
);
