

var ChallengeList = React.createClass({

    getInitialState: function() {
        return {
            events: [],
            solved_ids: []
        };
    },

    loadChallenges: function() {
        $.ajax({
            url: CHALLENGES_URL,
            dataType: "json",
            cache: false,
            success: function (data) {
                this.setState({
                    events: data.events,
                    solved_ids: data.solved_ids
                });
            }.bind(this),
            error: function(xhr, status, err) {
                this.setState({events: [], solved_ids: []});
                console.error(CHALLENGES_URL, status, err.toString());
            }.bind(this)
        })
    },

    componentDidMount: function() {
        this.loadChallenges();
        setInterval(this.loadChallenges, this.props.pollInterval)
    },

    render: function() {
        return (
            <div>
                <h1>Challenges</h1>

                <div className="alert alert-info">
                    All the solutions have to be written in Python 3
                </div>

                {this.state.events.map(function(event, index) {
                    return <Event key={index} event={event} solved_ids={this.state.solved_ids} />;
                }.bind(this))}
            </div>
        );
    }
});

var Event = React.createClass({
    render: function() {
        var headingClassString = this.props.event.public ? "" : "text-warning";

        return (
            <div>
                <div className="page-header">
                    <h2 className={headingClassString}>
                        {this.props.event.title} <small>{this.props.event.start_time}</small>
                    </h2>
                </div>

                <div className="row">
                    {this.props.event.challenges.map(function(challenge, index) {
                        return <Challenge key={index} challenge={challenge} solved={this.props.solved_ids.indexOf(challenge.id) >= 0} />;
                    }.bind(this))}
                </div>
            </div>
        );
    }
});

var Challenge = React.createClass({
    render: function() {
        var panelClasses = "panel panel-";
        panelClasses += this.props.challenge.public ? (this.props.solved ? "success" : "default") : "warning";

        var labelClasses = "label pull-right label-";
        labelClasses += this.props.solved ? "success" : "primary";

        var detail_url = CHALLENGE_DETAIL_URL.replace("/0", "/" + this.props.challenge.id);

        return (
            <div className="col-md-4 col-sm-6">
                <div className={panelClasses}>
                    <div className="panel-heading">
                        <h3 className="panel-title">
                            <span className={labelClasses}>
                                {this.props.challenge.calculated_points}
                            </span>
                            {this.props.challenge.title}
                        </h3>
                    </div>
                    <div className="panel-body challenge-body-short">
                        <div dangerouslySetInnerHTML={{ __html: marked(this.props.challenge.description, {sanitize: true}) }}></div>
                    </div>
                    <div className="list-group">
                        <a href={detail_url} className="list-group-item">Go to challenge</a>
                    </div>
                </div>
            </div>
        );
    }
});

ReactDOM.render(
  <ChallengeList pollInterval={30*1000} />,
  document.getElementById('challenges_list')
);
