import React, { Component } from 'react';
import {Button,Form, Row} from 'react-bootstrap'
import $ from 'jquery';
import { NivoAreaChart } from "../Charts/NivoAreaChart";
// import React, {useState, useEffect } from 'react'

class SearchIQS extends Component { 
    constructor (){
        super()
        this.g = this.g.bind(this)
        this.addMoreTweets = this.addMoreTweets.bind(this)
        this.search = this.search.bind(this)
        this.stopSearchs = this.stopSearchs.bind(this)
        
    }
    state = { 
        text: "",
        search_count: "",
        iterations: "",
        output_keywords_count:"",
        keywords_start_size:"",
        max_tweets_per_query: "",
        min_tweet_count:"",
        search_ids:[],
        id:""

       }
    async g (){
        console.log("####### g")
        // this.getSearchUpdates()
        // stopSearchs([search_ids.shift()]);//
        // $("#search_btn").prop('disabled', true);
        console.log("g function");
        // $("#result_container").attr("style", "display: none");
        // $("#tweets_container").empty();
        var data = {'prototype': $('#prototype').val()};
        // console.log(data)
        var temp_search_ids = this.state.search_ids
        var id=""
        var res =await fetch("/get_id", {
            method: "POST",
            body: JSON.stringify(data)})
        
       
            // console.log(response.json());
        var search_id = await res.json();
        // console.log(search_id)
        
        
            // console.log(this.state)
           
        temp_search_ids.push(search_id)
            // id = search_id
            // console.log("*****", id);
            // to_search(search_id, temp_search_ids)
            // temp_search_ids.push(search_id)
            
            
            // setSearchUpdatesListener(search_id);
            // runIQS(search_id);
            // wait_time = 1;

        // }).catch(function (err) {
        //     console.log(err);
        //     console.log("Booo2");
        //     // wait_time = wait_time * 2;
        //     // setTimeout(getSearchUpdates(), wait_time * 1000);
        // });
        // while(id == null){}
        // async function to_search(id, temp_search_ids){
        //     console.log("*****2", id)
            
        // }
        await this.search(search_id, temp_search_ids)
        

    }



    handleSubmit = async event =>{
          event.preventDefault();
          this.setState({text: event.target[0].value})
          this.setState({search_count: event.target[1].value})
          this.setState({iterations: event.target[2].value})
          this.setState({output_keywords_count: event.target[3].value})
          this.setState({keywords_start_size: event.target[4].value})
          this.setState({max_tweets_per_query: event.target[5].value})
          this.setState({min_tweet_count: event.target[6].value})
          this.setState({search_ids: []})
          // const {text, search_count,iterations} = this.state
        await this.g()

        //   console.log(text)
        //   const text = event.target[0].value
        //   const search_count = event.target[1].value
        //   const iterations = event.target[2].value

    }
    

    async search(search_id, temp_search_ids){
        console.log("####### search")
        console.log("search_id", search_id)
        // this.setState({search_ids : temp_search_ids})
        
        // console.log(search_id)
        const ophir ={method:'POST',body:JSON.stringify(
            {form:
                {text: this.state.text,
                    search_count: this.state.search_count,
                    iterations: this.state.iterations,
                    output_keywords_count: this.state.output_keywords_count,
                    keywords_start_size: this.state.keywords_start_size,
                    max_tweets_per_query: this.state.max_tweets_per_query,
                    min_tweet_count: this.state.min_tweet_count,
                    search_id: search_id
            
            }})
        , headers: { 'Content-Type': 'application/json' },};
        try{
            const response = await fetch('/search', ophir)
            await this.setState({id:search_id})
            // await this.addMoreTweets(search_id)
        //   const response = await axios.post(`/search`, body)
        //   console.log(response)
          if(response.status === 200){

            console.log("search complete")
          }
        }
        catch(e){
            console.log(e)
            }
        }

    // stopSearchs(searchs_ids) {
    //     var data = {'search_ids': searchs_ids};
    //     fetch("/close_search", {
    //         method: "POST",
    //         body: JSON.stringify(data)
    //     }).catch(function () {
    //         console.log("Booo3");
    //         wait_time = wait_time * 2;
    //         setTimeout(stopSearchs(searchs_ids), wait_time * 1000);
    //     });
    //     wait_time = 1;
    //     return null;
    // }
    async addMoreTweets() {
        console.log("*****" , "addMoreTweets")
        // console.log(search_id)
        // var $tweetsContainer = $("#tweets_container");
        // console.log($tweetsContainer);
        // let data = "data"
        // var data;
        var data = {"search_id": this.state.id}
        var res = await fetch("/load_results", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {'Content-Type': 'application/json' }})
        console.log(res)
        var tweet_htmls = await res.json()
        console.log(tweet_htmls)
        if (tweet_htmls.length > 0) {
            tweet_htmls.forEach(getTweetDiv);

            function getTweetDiv(tweet_html) {
                var $div = $("<div>", {"class": "col-md-6"});
                $div.html(tweet_html);
                $('#tweetsContainer').append($div);
            }
        } else {
            $("#load_more_btn").hide();
        }
        console.log("tweet_htmlss")
        console.log(tweet_htmls)
        // $("#result_container").style.display = "block"
        // $("#result_container").attr(style={{display:block}});
        // search_id.then(result => {
        //     return {"search_id": result}}).then((data)=>{
        //         console.log(data)
        //         fetch("/load_results", {
        //         method: "POST",
        //         body: JSON.stringify(data),
        //         headers: {'Content-Type': 'application/json' }
        //     }).then((res)=>{
        //         return res.json()
        //     }).then((tweet_htmls)=>{
        //         console.log("tweet_Html", tweet_htmls)
        //         if (tweet_htmls.length > 0) {
        //             // tweet_htmls.forEach(getTweetDiv);
    
        //             // function getTweetDiv(tweet_html) {
        //             //     var $div = $("<div>", {"class": "col-md-12"});
        //             //     $div.html(tweet_html);
        //             //     $tweetsContainer.append($div);
        //             // }
        //         } else {
        //             $("#load_more_btn").hide();
        //         }
        //     })
           
 
        //     // console.log("inside")
        //     // console.log(data)
        // })
        
        // // console.log("outside")
        // // console.log(this.state.data)
        // // console.log(data)
    }
    
    getSearchUpdates = async () =>{
        this.stopSearchs();//
        // $("#search_btn").prop('disabled', true);
        console.log("getSearchUpdates");
        // $("#result_container").attr("style", "display: none");
        // $("#tweets_container").empty();
        var data = {'prototype': $('#prototype').val()};
        // console.log(data)
        fetch("/get_id", {
            method: "POST",
            body: JSON.stringify(data)
        }).then(function (response) {
            // console.log(response.json());
            return response.json();
        }).then(function (search_id) {
            console.log(search_id);  
            let temp_search_ids = this.state.search_ids
            temp_search_ids.push(search_id)
            this.setState({search_ids : temp_search_ids})
            
            // setSearchUpdatesListener(search_id);
            // runIQS(search_id);
            // wait_time = 1;

        }).catch(function (err) {
            console.log(err);
            console.log("Booo2");
            // wait_time = wait_time * 2;
            // setTimeout(getSearchUpdates(), wait_time * 1000);
        });

    
    }

    stopSearchs = async()=> {
        console.log("stopSearchs")
        this.state.search_ids.shift()
        var data = {'search_ids': this.state.search_ids};
        fetch("/close_search", {
            method: "POST",
            body: JSON.stringify(data)
        }).catch(function () {
            console.log("Booo3");
            // wait_time = wait_time * 2;
            setTimeout(this.stopSearchs(), 10 * 1000);
        });
        // wait_time = 1;
        return null;
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
            <Form onSubmit={this.handleSubmit} >
            <div class="form-group row justify-content-md-center">
            <label for="textarea" class="col-2 col-form-label">Text Area</label>
            <div class="col-5">
                <textarea 
			 id="prototype" name="prototype" cols="40" rows="5" class="form-control"
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
                <input id="iterations" name="iterations"  type="number" defaultValue={2} class="form-control"
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
  <Button class="Button" id="search_btn" variant="primary" type="submit" >
    Submit
  </Button>
  <Button class="Button" id="load" variant="primary" onClick={this.addMoreTweets} >
    load more
  </Button>
</Form>
<div id="result_container" >
<div class="row" id="tweetsContainer">

</div>
</div>
<div className="App-charts">
{/* <NivoAreaChart /> */}

</div>

</div>;
    }
}
 
export default SearchIQS;