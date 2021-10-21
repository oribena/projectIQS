import SearchIQS from "../components/SearchIQS"
import React, { Component } from 'react';

class SearchPage extends React.Component {
    render() { 

        return <div>
            <h1>Iterative Query Selection </h1>
            This dashboard demonstrates the iterative query selection method.
            <SearchIQS></SearchIQS>

        </div>;
    }
}
 
export default SearchPage;