import './App'
import 'react'
import 'react-dom'
import App
import React
import ReactDOM

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});
