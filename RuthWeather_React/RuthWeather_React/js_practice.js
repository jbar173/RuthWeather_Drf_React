import React from 'react';
import './App.css';


class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      weatherReportToday: [],
      am: [],
      pm: [],
      eve: [],
      // weatherReport:{
      //   id:null,
      //   date:'',
      //   outlook:'',
      //   am:'', ////// make an api call to retrieve Am with this pk
      //   pm:'',///////  " " pm pk
      //   eve:'', ////// " " eve pk
      // },
      // amReport:{
      //   temp:'',
      //   prec:'',
      // },
      // pmReport:{
      //   temp:'',
      //   prec:'',
      // },
      // eveReport:{
      //   temp:'',
      //   prec:'',
      // },
    editing:false,
    }
    this.fetchWeather = this.fetchWeather.bind(this)
    this.fetchSections = this.fetchSections.bind(this)
    this.getCookie = this.getCookie.bind(this)
};


// functions:-

getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }


componentWillMount(){
    this.fetchWeather()
    this.fetchSections()
  }

fetchWeather(){
  console.log("Fetching...")

  fetch('http://127.0.0.1:8000/api/main-report/')
  .then(response => response.json())
  .then(data =>
    this.setState({
      weatherReportToday:data
    })
  )
}

fetchSections(weatherReportToday){
  var report = weatherReportToday[0]
  fetch(`http://127.0.0.1:8000/api/am-detail/${report.am.id}/`)
  .then(response => response.json())
  .then(data =>
    this.setState({
      am:data
    })
  )
  fetch(`http://127.0.0.1:8000/api/pm-detail/${report.pm.id}/`)
    .then(response => response.json())
    .then(data =>
      this.setState({
        pm:data
      })
    )
  fetch(`http://127.0.0.1:8000/api/eve-detail/${report.eve.id}/`)
  .then(response => response.json())
  .then(data =>
    this.setState({
      eve:data
    })
  )
}


    render(){
      var report = this.state.weatherReportToday
      var am_rep = this.state.am
      var pm_rep = this.state.pm
      var eve_rep = this.state.eve

      return(

  ////// if settings.day_mode:
        <div className="container base-day" style={{height:'100vh'}}>

          <div className="container outer">

              <div className="row title">
                <div className="col-12">

                </div>
              </div>

              <div className="row info">
                  <div className="col-6-l report left-column">
                      <h3>{report.date}</h3>
                      <p>{report.outlook}</p>

                      <p>{am.temp}</p>
                      <p>{am.prec}</p>

                      <p>{pm.temp}</p>
                      <p>{pm.prec}</p>

                      <p>{eve.temp}</p>
                      <p>{eve.prec}</p>

                  </div>

                  <div className="col-6-r settings right-column">


                  </div>

              </div>

           </div>
        </div>
      )
    }
  }

export default App;
