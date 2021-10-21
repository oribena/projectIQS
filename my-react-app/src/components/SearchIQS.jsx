import React, { Component } from 'react';
import {Button,Form, Row} from 'react-bootstrap'
import axios from 'axios';
import $ from 'jquery';
// import React, {useState, useEffect } from 'react'

class SearchIQS extends Component { 
    state = { 
        text: "",
        search_count: "",
        iterations: "",
        output_keywords_count:"",
        keywords_start_size:"",
        max_tweets_per_query: "",
        min_tweet_count:"",
        search_ids:[]

       }

    handleSubmit = event =>{
          event.preventDefault();
          this.setState({text: event.target[0].value})
          this.setState({search_count: event.target[1].value})
          this.setState({iterations: event.target[2].value})
          this.setState({output_keywords_count: event.target[3].value})
          this.setState({keywords_start_size: event.target[4].value})
          this.setState({max_tweets_per_query: event.target[5].value})
          this.setState({min_tweet_count: event.target[6].value})
          // const {text, search_count,iterations} = this.state
          this.g()

        //   console.log(text)
        //   const text = event.target[0].value
        //   const search_count = event.target[1].value
        //   const iterations = event.target[2].value

    }
    g = async ()=>{

        const ophir ={method:'POST',body:JSON.stringify(
            {form:
                {text: this.state.text,
                    search_count: this.state.search_count,
                    iterations: this.state.iterations,
                    output_keywords_count: this.state.output_keywords_count,
                    keywords_start_size: this.state.keywords_start_size,
                    max_tweets_per_query: this.state.max_tweets_per_query,
                    min_tweet_count: this.state.min_tweet_count,
            
            }})
        , headers: { 'Content-Type': 'application/json' },};
        try{
            const response = await fetch('/search', ophir)
        //   const response = await axios.post(`/search`, body)
          console.log(response)
          if(response.status === 200){
            console.log(response.data)
          }
        }
        catch(e){
            console.log(e)
            }

    }

    async search(){
      // text: "",
      // search_count: "",
      // iterations: "",
      // output_keywords_count:"",
      // keywords_start_size:"",
      // max_tweets_per_query: "",
      // min_tweet_count:"",
        const body ={method:'POST', body:JSON.stringify({form: 5})};
        try{
            const response = await fetch('/search', body)
        //   const response = await axios.post(`/search`, body)
          console.log(response)
          if(response.status === 200){
            console.log(response.data)
          }
        }
        catch(e){
            console.log(e)
            }
      }

    render() { 
        return <div className='body-container'>
          <link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"
  integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU"
  crossorigin="anonymous"
/>
{/*     
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> */}
            <Form onSubmit={this.handleSubmit}>
            <div class="form-group row justify-content-md-center">
            <label for="textarea" class="col-2 col-form-label">Text Area</label>
            <div class="col-5">
                <textarea id="prototype" name="prototype" cols="40" rows="5" class="form-control"
                          placeholder="Paste prototype document here..."></textarea>
            </div>
        </div>
        <br/>
        <div class="form-group row justify-content-md-center">
            <label for="search_count" class="col-2 col-form-label">Search Count</label>
            <div class="col-5">
                <input id="search_count" name="search_count"  type="number" defaultValue={1} class="form-control"
                       required="required"/>
            </div>
        </div>
        <br/>
        <div class="form-group row justify-content-md-center">
            <label for="iterations" class="col-2 col-form-label">Iterations</label>
            <div class="col-5">
                <input id="iterations" name="iterations"  type="number" defaultValue={15} class="form-control"
                       required="required"/>
            </div>
        </div>
        <br/>
        <div class="form-group row justify-content-md-center">
            <label for="output_keywords_count" class="col-2 col-form-label">Output Keywords Count</label>
            <div class="col-5">
                <input id="output_keywords_count" name="output_keywords_count" type="number" defaultValue={3}
                       class="form-control" required="required"/>
            </div>
        </div>
        <br/>
        <div class="form-group row justify-content-md-center">
            <label for="keywords_start_size" class="col-2 col-form-label">Keywords Start Size</label>
            <div class="col-5">
                <input id="keywords_start_size" name="keywords_start_size" type="number" defaultValue={3}
                       class="form-control" required="required"/>
            </div>
        </div>
        <br/>
        <div class="form-group row justify-content-md-center">
            <label for="max_tweets_per_query" class="col-2 col-form-label">Max Tweets Per Query</label>
            <div class="col-5">
                <input id="max_tweets_per_query" name="max_tweets_per_query" type="number" defaultValue={50}
                       class="form-control" required="required"/>
            </div>
        </div>
        <br/>
        <div class="form-group row justify-content-md-center">
            <label class="col-2 col-form-label" for="min_tweet_count">Min Tweet Count</label>
            <div class="col-5">
                <input id="min_tweet_count" name="min_tweet_count"  type="number" defaultValue={3} class="form-control"
                       required="required"/>
            </div>
        </div>
        <br/>
        <br/>
  <Button variant="primary" type="submit">
    Submit
  </Button>
</Form>


</div>;
    }
}
 
export default SearchIQS;