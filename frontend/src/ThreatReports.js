import React from 'react';

const ThreatReports = ({ reports }) => {
    return (
        <div>
            <h1>Threat Reports</h1>
            {reports.map((report, index) => (
                <div key={index}>
                    <h3>{report.title}</h3>
                    <p>{report.description}</p>
                </div>
            ))}
        </div>
    );
};

export default ThreatReports;
