// React view stuff
var cols = [
	{ key: 'address', label: 'IP Address' },
	{ key: 'current_bitrate', label : 'Bitrate' }
	];


var Table = React.createClass({
    render: function() {
        var headerComponents = this.generateHeaders(),
            rowComponents = this.generateRows();

        return (
            <table>
                <thead> {headerComponents} </thead>
                <tbody> {rowComponents} </tbody>
            </table>
        );
    },

    generateHeaders: function() {
        var cols = this.props.cols;  // [{key, label}]

        // generate our header (th) cell components
        return cols.map(function(colData) {
            return <th key={colData.key}> {colData.label} </th>;
        });
    },

    generateRows: function() {
        var cols = this.props.cols,  // [{key, label}]
            data = this.props.data;

        return data.map(function(item) {
            // handle the column data within each row
            var cells = cols.map(function(colData) {

                // colData.key might be "firstName"
                return <td> {item[colData.key]} </td>;
            });
            return <tr> {cells} </tr>;
        });
    }
});

function refreshTable(data) {
    console.log("data is", data);
    ReactDOM.render(<Table cols={cols} data={data}/>, document.getElementById('table'));
}

// Open the websocket
var socket = io();

// Handle websocket communications
socket.on('json', function(data) {
    refreshTable(data.results);
});

socket.on('error', console.error.bind(console));
socket.on('message', console.log.bind(console));

