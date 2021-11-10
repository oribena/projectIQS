import React, { Component } from "react";
import { ResponsiveLine } from "@nivo/line";
import moment from "moment";
import styles from "./styles.js";
import { nivoData } from "../util";

export class NivoAreaChart extends Component {
  state = {
    // data: nivoData()
  };
  customTooltip = ({ point }) => {
    return (
      <p style={styles.tooltip}>
        Time: <b>1</b>
        <br />
        Count: <b>{point.data.yFormatted}</b>
      </p>
    );
  };
  render() {
    return (
      // make sure parent container have a defined height when using
      <div style={styles.container}>
        <h3 style={styles.title}>Nivo Stacked Area Chart</h3>
        <ResponsiveLine
          animate
          data={this.props.data}
          margin={{ top: 24, right: 96, bottom: 72, left: 64 }}
          xFormat={d => d}
          xScale={{ type: "time", format: "native" }}
          yScale={{
            type: "linear",
            min: 0,
            max: 200,
            stacked: true
          }}
          curve="natural"
          tooltip={this.customTooltip}
          colors={{ scheme: "purpleRed_green" }}
          lineWidth={1}
          pointSize={4}
          enableArea={true}
          useMesh={true}
        />
      </div>
    );
  }
}