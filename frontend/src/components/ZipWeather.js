import React from "react";
import axios from "axios";
import {HOST_URL} from "../settings";

class ZipWeather extends React.Component {
  state = {
    zipCode: "",
    weatherData: null,
    favouriteZipCodes: new Set(),
    suggestedFavouriteZipCodes: [],
  }

  componentDidMount() {
    axios.get(`${HOST_URL}/favourite_zip_codes`)
      .then(res => {
        this.setState({
          favouriteZipCodes: new Set(res.data),
        })
      })
      .catch(err => console.log("error " + err))
  }

  searchFavouriteZipCodes = (search) => {  // for suggestions
    axios.get(`${HOST_URL}/favourite_zip_codes`,
      {params: {search: search, limit: 5}}
    )
      .then(res => {
        this.setState({
          suggestedFavouriteZipCodes: res.data,
        })
      })
      .catch(err => console.log("error " + err))
  }

  handleChange = e => {
    this.setState({zipCode: e.target.value});
  };

  getWeatherInfo = (zipCode) => {
    axios.get(`${HOST_URL}/weather_info/${zipCode}`)
      .then(res => {
        this.setState({
          weatherData: {
            'zipCode': res.data['zip_code'],
            'detailedStatus': res.data['detailed_status'],
            'temperature': res.data['temperature'],
            'windSpeed': res.data['wind_speed'],
            'pressure': res.data['pressure'],
            'humidity': res.data['humidity'],
            'locationName': res.data['location_name'],
          },
        })
      })
      .catch(err => console.log("error " + err))
  }

  handleSubmit = e => {
    e.preventDefault();
    this.getWeatherInfo(this.state.zipCode);
  };

  addToFavourites = zipCode => {
    axios.post(`${HOST_URL}/favourite_zip_code/${zipCode}`)
      .then(res => {
        let newFavouriteZipCodes = this.state.favouriteZipCodes.add(res.data)
        this.setState({
          favouriteZipCodes: newFavouriteZipCodes,
        })
      })
      .catch(err => console.log("error " + err))
  }

  removeFromFavourites = zipCode => {
    axios.delete(`${HOST_URL}/favourite_zip_code/${zipCode}`)
      .then(() => {
        let newFavouriteZipCodes = this.state.favouriteZipCodes;
        newFavouriteZipCodes.forEach(obj => {
          if (obj.code === zipCode) {
            newFavouriteZipCodes.delete(obj);
          }
        })

        this.setState({
          favouriteZipCodes: newFavouriteZipCodes,
        })
      })
      .catch(err => console.log("error " + err))
  }

  render() {
    const {favouriteZipCodes, weatherData} = this.state

    return (
      <div className="container">
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <button className="navbar-toggler" type="button" data-toggle="collapse"
                  data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                  aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"/>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item active"/>
              <li className="nav-item"/>
              <li className="nav-item"/>
            </ul>
            <form className="form-inline my-2 my-lg-0"
                  _lpchecked="1"
                  onSubmit={this.handleSubmit}>
              <input
                className="form-control mr-sm-2"
                type="text"
                placeholder="Zip Code"
                aria-label="Zip Code"
                onChange={this.handleChange}
              />
              <button className="btn btn-outline-success my-2 my-sm-0" type="submit">
                Search
              </button>
            </form>
          </div>
        </nav>
        <footer className="footer">
          <ul className="list-group">

            {[...favouriteZipCodes].map((zipCode, index) =>
              <li key={index}
                  className="list-group-item"
                  onClick={() => this.getWeatherInfo(zipCode.code)}>
                {zipCode.code}
                <button type="button"
                        className="btn btn-default"
                        style={{display: 'inline', float: 'right'}}
                        onClick={() => this.removeFromFavourites(zipCode.code)}>
                  X
                </button>
              </li>
            )}

          </ul>

          {weatherData ?
            <p contentEditable="true" spellcheckker="false">
              <div className="card" style={{marginTop: '30px'}}>
                <div className="card" style={{marginTop: '0px'}}>
                  <div className="card-body" style={{marginTop: '0px'}}>
                    <h4 className="card-title">
                      <b>{weatherData.locationName}</b>
                    </h4>
                    <div className="row">
                      <div className="col-sm-4">
                        <h1>
                          {weatherData.temperature}°
                          <h6>{weatherData.detailedStatus}</h6>
                        </h1>
                      </div>
                      <div className="col-sm-4 col-5">
                        <h3/>
                      </div>
                      <div className="col-sm-4">
                        <h5>Pressure {weatherData.pressure}</h5>
                        <h5>Humidity {weatherData.humidity}%</h5>
                        <h5>Wind {weatherData.windSpeed} mph</h5>
                        <div className="row">
                          <div className="col-sm-4"/>
                          <div className="col-sm-4 col-5"/>
                          <div className="col-sm-4"/>
                        </div>
                      </div>
                    </div>
                    <a href="#"
                       className="btn btn-primary"
                       onClick={() => this.addToFavourites(weatherData.zipCode)}>
                      Add to favorites
                    </a>

                  </div>
                </div>
              </div>
              © Firstly NodeJS 2021
            </p>
            :
            <React.Fragment/>
          }

        </footer>
      </div>
    );
  }
}

export default ZipWeather;
