import React from 'react';
import './App.css';
import { FaMoon } from 'react-icons/fa';
import { FaSun } from 'react-icons/fa';


class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      mode:true,
      current:false,
      cityList:[],
      updateReportForm:{
        city:'',
      },
      activeReport:{id:'',date:'',
        city:'',outlook:'',
        eve_temp:'',am:'',
        pm:'',eve:'',
        city_objects:[], },
      activeCity:{id:'',
        name:'',latitude:'',
        longitude:'',
      },
      activeAm:{id:'',
        date:'',temp:'',
        prec:'', },
      activePm:{id:'',
        date:'',temp:'',
        prec:'', },
      activeEve:{id:'',
        date:'',temp:'',
        prec:'', },
      editing:false,
    }
    this.fetchWeather = this.fetchWeather.bind(this)
    this.fetchCity = this.fetchCity.bind(this)
    this.fetchAm = this.fetchAm.bind(this)
    this.fetchPm = this.fetchPm.bind(this)
    this.fetchEve = this.fetchEve.bind(this)
    this.fetchCityList = this.fetchCityList.bind(this)
    this.getCookie = this.getCookie.bind(this)

    this.set_mode = this.set_mode.bind(this)
    this.expand_collapse = this.expand_collapse.bind(this)

    this.handleCity = this.handleCity.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleClear = this.handleClear.bind(this)
    this.handleClearSubmit = this.handleClearSubmit.bind(this)

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

componentDidMount(){
    this.fetchWeather()
  }

fetchWeather(){
  console.log("Fetching...")
  fetch('http://127.0.0.1:8000/api/report-main')
  .then(response => response.json(), reject => console.log('Error: ', reject))
  .then(data =>
    this.setState({
      activeReport:data
    })
  )
}

componentDidUpdate(){

  if(this.state.activeCity.id !== this.state.activeReport.city){
        this.fetchCity(this.state.activeReport);}
  if(this.state.activeAm.id !== this.state.activeReport.am){
        this.fetchAm(this.state.activeReport);}
  if(this.state.activePm.id !== this.state.activeReport.pm){
        this.fetchPm(this.state.activeReport);}
  if(this.state.activeEve.id !== this.state.activeReport.eve){
        this.fetchEve(this.state.activeReport);
        this.fetchCityList(this.state.cityList);}
}

fetchCity(report){
  var url = `http://127.0.0.1:8000/api/city-detail/${report.city}`
  fetch(url)
  .then(response => response.json(), reject => console.log('Error: ', reject))
  .then(data =>
    this.setState({
      activeCity:data
    })
  )
}

fetchAm(report){
  var url = `http://127.0.0.1:8000/api/am-detail/${report.am}`

  fetch(url)
  .then(response => response.json(), reject => console.log('Error: ', reject))
  .then(data =>
    this.setState({
      activeAm:data
    })
  )
}

fetchPm(report){
  fetch(`http://127.0.0.1:8000/api/pm-detail/${report.pm}`)
    .then(response => response.json(), reject => console.log('Error: ', reject))
    .then(data =>
      this.setState({
        activePm:data
      })
    )
}

fetchEve(report){
  fetch(`http://127.0.0.1:8000/api/eve-detail/${report.eve}`)
  .then(response => response.json(), reject => console.log('Error: ', reject))
  .then(data =>
    this.setState({
      activeEve:data
    })
  )
}

fetchCityList(){
  fetch(`http://127.0.0.1:8000/api/city-list`)
    .then(response => response.json())
    .then(data =>
      this.setState({
        cityList:data
      })
    )
}

set_mode(mode){
  if(mode === true){
    console.log("Switching to night mode");
    this.setState({
      mode:false
    })
  }else{
    console.log("Switching to day mode");
    this.setState({
      mode:true
    })
  }
}

expand_collapse(current){
  if(current === false){
    console.log("**expand click")
    this.setState({
      current:true
    })
  }else{
    console.log("**collapse click")
    this.setState({
      current:false
    })
  }
}

handleCity(e){
  console.log("one")
  e.stopPropagation()
  var value = e.target.name
  console.log("var value: " + value)
  this.setState({
    updateReportForm:{
      ...this.state.updateReportForm,
      city:value
    }
  })
}

handleChange(e){
  console.log("two")
  e.stopPropagation()
  var value = e.target.value
  console.log("var value: " + value)
  this.setState({
    updateReportForm:{
      ...this.state.updateReportForm,
      city:value
    }
  })
}

handleSubmit(e){
  console.log("Four")
  e.preventDefault()
  var csrftoken = this.getCookie('csrftoken')
  var url = 'http://127.0.0.1:8000/api/report-main'

  console.log("submitting")
  fetch(url, {
    method:'POST',
    headers:{
      'Content-type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify(this.state.updateReportForm)
  }).then((response) => {
      this.fetchWeather()
      this.setState({
        updateReportForm:{
          city:'',
        }
    })
  })
}

handleClear(e){
  var value = e.target.name
  console.log("clear clicked")
  console.log("var value: " + value)

  this.setState({
    updateReportForm:{
      ...this.state.updateReportForm,
      city:value
      }
  })
}

handleClearSubmit(e){
  e.preventDefault()
  console.log("clear submit")
  var csrftoken = this.getCookie('csrftoken')
  var url = 'http://127.0.0.1:8000/api/report-main'

  fetch(url, {
    method:'POST',
    headers:{
      'Content-type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify(this.state.updateReportForm)
  }).then((response) => {
      this.fetchWeather()
      this.setState({
        updateReportForm:{
          city:'',
        }
    })
  })
}

    render(){
      var report = this.state.activeReport
      var cities = this.state.cityList
      var city_rep = this.state.activeCity
      var am_rep = this.state.activeAm
      var pm_rep = this.state.activePm
      var eve_rep = this.state.activeEve
      var mode = this.state.mode
      var current = this.state.current
      var self = this


      return(

      <div className="container" style={{height:'100vh'}}>

        {mode===true ?
          (<div id="outer-div-day" className="container outer day-mode">

              <div className="row title">
                      <div className="col-12">
                        <h1>Welcome to RuthWeather!</h1>
                        <h2>Report for {city_rep.name} today ({report.date})</h2>
                      </div>
              </div>

              <div className="row info">

                      <div className="col-6-l report left-column">

                              <div className="outline">
                              <h2>Outlook for today:</h2> <p>{report.outlook}.</p>
                              </div>

                                <div className="outline">
                                  <h2>Morning:</h2>
                                  <span><h4>Average temperature: </h4><p>{am_rep.temp} degrees celcius</p></span>
                                  <span><h4>Average precipitation: </h4><p>{am_rep.prec}% chance</p></span>
                                </div>

                                <div className="outline">
                                  <h2>Afternoon:</h2>
                                  <span><h4>Average temperature: </h4><p>{pm_rep.temp} degrees celcius</p></span>
                                  <span><h4>Average precipitation: </h4><p>{pm_rep.prec}% chance</p></span>
                                </div>

                                <div className="outline">
                                  <h2>Evening:</h2>
                                  <span><h4>Average temperature: </h4><p>{eve_rep.temp} degrees celcius</p></span>
                                  <span><h4>Average precipitation: </h4><p>{eve_rep.prec}% chance</p></span>
                                </div>
                       </div>

                      <div className="col-6-r settings right-column">

                              <div className="slider" onClick={() => self.set_mode(mode)}>
                                  {mode===true ? (<span><FaMoon className="moon"/></span>)
                                    : (<span><FaSun className="sun"/></span>)
                                  }
                              </div>

                                  <div id="expand" onClick={() => self.expand_collapse(current)}>
                                    {current === false ?
                                      (<button type="button" className="button-border-day button-day-size" style={{cursor:"pointer",}}>Change city</button>)
                                                        :
                                       (<div>
                                         <h3 className="button-border-day" style={{cursor:"pointer"}}>Select a city:</h3>
                                          <form>
                                            <div className="city-list">
                                             {cities.map((city,index) => {
                                               return(
                                                     <div key={index}>
                                                        <button id="button-day" value="submit" name={city.name} onClick={this.handleCity}
                                                         type="button" style={{cursor:"pointer"}}>{city.name}</button>
                                                     </div>
                                                 )
                                               })}
                                               </div>
                                               <h3 className="button-border-day new-city">Or type new city:</h3>

                                               <input onClick={this.handleChange} onChange={this.handleChange} placeholder="Add a new city"
                                                 className="form-control" value={this.state.updateReportForm.city}
                                                 type="text" id="button-day"/>
                                               <input className="margin-top" onClick={this.handleSubmit} type="submit" id="button-day" value="Go"/>

                                            </form>

                                        </div>

                                     )
                                   }
                          </div>
                          <form onSubmit={this.handleClearSubmit}>
                            <button className="button-padding clear-city-day" name="true" id="button-day" style={{cursor:"pointer"}} onClick={this.handleClear}>Clear City List</button>
                          </form>
                      </div>
                  </div>
            </div> )

            : (<div id="outer-div-night" className="container outer night-mode">

                    <div className="row title">
                          <div className="col-12">
                            <h1>Welcome to RuthWeather!</h1>
                            <h2>Report for {city_rep.name} today ({report.date})</h2>
                          </div>
                    </div>

                  <div className="row info">

                          <div className="col-6-l report left-column">

                                <div className="outline">
                                <h2>Outlook for today:</h2> <p>{report.outlook}.</p>
                                </div>

                                <div className="outline">
                                  <h2>Morning:</h2>
                                  <span><h4>Average temperature: </h4><p>{am_rep.temp} degrees celcius</p></span>
                                  <span><h4>Average precipitation: </h4><p>{am_rep.prec}% chance</p></span>
                                </div>

                                <div className="outline">
                                  <h2>Afternoon:</h2>
                                  <span><h4>Average temperature: </h4><p>{pm_rep.temp} degrees celcius</p></span>
                                  <span><h4>Average precipitation: </h4><p>{pm_rep.prec}% chance</p></span>
                                </div>

                                <div className="outline">
                                  <h2>Evening:</h2>
                                  <span><h4>Average temperature: </h4><p>{eve_rep.temp} degrees celcius</p></span>
                                  <span><h4>Average precipitation: </h4><p>{eve_rep.prec}% chance</p></span>
                                </div>

                           </div>

                          <div className="col-6-r settings right-column">

                                      <div className="slider" onClick={() => self.set_mode(mode)}>
                                          {mode===true ? (<span><FaMoon /></span>)
                                            : (<span><FaSun className="sun"/></span>)
                                          }
                                      </div>

                                      <div id="expand" onClick={() => self.expand_collapse(current)}>
                                        {current === false ?
                                          (<button type="button" id="button-night" style={{cursor:"pointer"}}>Change City</button>)
                                                            :
                                           (<div>
                                             <h3 style={{cursor:"pointer"}}>Select a city:</h3>
                                              <form>
                                                 {cities.map((city,index) => {
                                                   return(
                                                         <div key={index}>
                                                            <button id="button-night" name={city.name} onClick={this.handleCity}
                                                             type="button" style={{cursor:"pointer"}}>{city.name}</button>
                                                         </div>
                                                         )
                                                       })}
                                                       <h3>Or type new city:</h3>
                                                   <input onClick={this.handleChange} onChange={this.handleChange} placeholder="Add a new city"
                                                   className="form-control" value={this.state.updateReportForm.city}
                                                   type="text" id="button-night"/>
                                                  <input onClick={this.handleSubmit} type="submit" value="Go" id="button-night"/>
                                                </form>

                                            </div>
                                          )
                                        }
                                  </div>
                                  <form onSubmit={this.handleClearSubmit}>
                                    <button className="button-padding" name="true" id="button-night" style={{cursor:"pointer"}} onClick={this.handleClear}>Clear City List</button>
                                  </form>
                          </div>
                      </div>
                 </div>)}
        </div>
      )
  }
}


export default App;
