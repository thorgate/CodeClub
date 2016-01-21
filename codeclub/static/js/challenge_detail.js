

var ChallengeDetail = React.createClass({

    getInitialState: function() {
        return {
            challenge: "loading",
            solutions: []
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
                    solutions: data.solutions
                });
            }.bind(this),
            error: function(xhr, status, err) {
                this.setState({challenge: null, solutions: []});
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

                <div className="label label-danger pull-right">Wrong</div>
                <div className="label label-warning pull-right">Timed out</div>
                <div className="label label-info pull-right">In progress</div>
                <div className="label label-success pull-right">Correct</div>

                <h2>Your solutions</h2>

                <SolutionList solutions={this.state.solutions} />
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
        var solutionClass = "list-group-item";
        if (this.props.solution.bootstrap_class) {
            solutionClass += " list-group-item-" + this.props.solution.bootstrap_class
        }

        return (
            <a href={ this.props.solution.url } className={solutionClass}>
                <span className="pull-right">
                    { this.props.solution.timestamp }
                </span>

                { this.props.solution.filename }
            </a>
        );
    }
});

ReactDOM.render(
  <ChallengeDetail pollInterval={5*1000} url={CHALLENGE_URL} />,
  document.getElementById('challenge_detail')
);
