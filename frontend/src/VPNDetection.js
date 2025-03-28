import React from 'react';

const VPNDetection = ({ vpnData }) => {
    return (
        <div>
            <h1>VPN Detection Results</h1>
            <table>
                <thead>
                    <tr>
                        <th>IP Address</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {vpnData.map((item, index) => (
                        <tr key={index}>
                            <td>{item.ip}</td>
                            <td>{item.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default VPNDetection;
