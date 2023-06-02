var config = {
    content: [{
        type: 'row',
        content: [
            {
                title: 'A react component',
                type: 'react-component',
                component: 'testItem',
                props: { value: 'I\'m on the left' }
            },
            {
                title: 'Another react component',
                type: 'react-component',
                component: 'testItem'
            }
        ]
    }]
};


var myLayout = new GoldenLayout(config);

myLayout.registerComponent('testItem', React.createClass({
    getInitialState: function () {
        return { value: this.props.value || 'bla' };
    },
    setValue: function (e) {
        this.setState({ value: e.target.value });
    },
    setContainerTitle: function () {
        this.props.glContainer.setTitle(this.state.value);
    },
    render: function () {
        return (
            <div>
                <input type="text" value={this.state.value} onChange={this.setValue} />
                <button onClick={this.setContainerTitle}>set title</button>
            </div>
        )
    }
}));

myLayout.init();