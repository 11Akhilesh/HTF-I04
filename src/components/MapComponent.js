
import React from 'react';
import { useState, useEffect } from 'react';
import { LoadScript, GoogleMap, DirectionsRenderer } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '500px',
  margin: '20px 0'
};

const center = {
  lat: 20.5937,
  lng: 78.9629
};

const MapComponent = ({ source, destination, routeSegments }) => {
  const [directions, setDirections] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (window.google && routeSegments && routeSegments.length > 0) {
      const directionsService = new window.google.maps.DirectionsService();
      
      // Create waypoints from segments
      const waypoints = routeSegments.slice(1, -1).map(segment => ({
        location: segment.from,
        stopover: true
      }));

      directionsService.route({
        origin: routeSegments[0].from,
        destination: routeSegments[routeSegments.length - 1].to,
        waypoints: waypoints,
        travelMode: window.google.maps.TravelMode.DRIVING,
        optimizeWaypoints: true
      }, (result, status) => {
        if (status === 'OK') {
          setDirections(result);
        } else {
          setError(`Error fetching directions: ${status}`);
        }
      });
    }
  }, [routeSegments]);

  return (
    <LoadScript googleMapsApiKey="AIzaSyDzggQCozVlD6dhbw5JJYi5YC6YWT_25FU">
      <div style={containerStyle}>
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={center}
          zoom={5}
        >
          {directions && <DirectionsRenderer directions={directions} />}
        </GoogleMap>
      </div>
    </LoadScript>
  );
};

export default React.memo(MapComponent);
