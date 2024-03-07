import React, {useState} from 'react'
import {Button, CloseButton} from 'react-bootstrap'
import './SearchBar.css'

function SearchBar({onSearch}) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="input-group">
        <input
          type="text"
          placeholder="Search movies..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />
        <CloseButton className="close-button" onClick={() => setQuery("")} />
      </div>
      <Button variant="primary" size="sm" type="submit">
        Search
      </Button>
    </form>
  );
}

export default SearchBar
