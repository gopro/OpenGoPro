// Create combined search store
let store = jekyllStore.concat(specStore);

// Build the store
let idx = lunr(function () {
    this.field('title');
    this.field('excerpt');
    this.ref('id');
    this.metadataWhitelist = ['position'];

    for (let item in store) {
        this.add({
            title: store[item].title,
            excerpt: store[item].excerpt,
            id: item,
        });
    }
});

const SNIPPET_LEN = 200;

$(document).ready(function () {
    $('input#search').on('keyup', function () {
        // Build and perform the search
        let resultdiv = $('#results');
        let query = $(this).val().toLowerCase();
        let results = idx.query(function (q) {
            // Biggest boost goes to complete phrase in title
            q.term(query, { fields: ['title'], boost: 100 });
            // Actual search term in excerpt with no wildcards get a boost
            q.term(query, { fields: ['excerpt'], boost: 50 });
            // Now add terms for individual words
            query.split(lunr.tokenizer.separator).forEach(function (term) {
                // Actual search term in title with no wildcards get a boost
                q.term(term, { fields: ['title'], boost: 10 });
                // Title Term with wildcards gets a smaller boost
                if (query.lastIndexOf(' ') != query.length - 1) {
                    q.term(term, {
                        fields: ['title'],
                        wildcard: lunr.Query.wildcard.TRAILING,
                        boost: 5,
                    });
                }
                // Actual search term in excerpt with no wildcards get a boost
                q.term(term, { fields: ['excerpt'], boost: 5 });
                // excerpt Term with wildcards gets a smaller boost
                if (query.lastIndexOf(' ') != query.length - 1) {
                    q.term(term, {
                        fields: ['title'],
                        wildcard: lunr.Query.wildcard.TRAILING,
                        boost: 1,
                    });
                }
                // TODO currently not using any fuzziness
                // Add fuzziness of 1 character change with no boost
                // if (term != '') {
                //     q.term(term, { fields: ['excerpt'], editDistance: 1 });
                // }
            });
        });
        // Build and display the results
        resultdiv.empty();
        resultdiv.prepend(
            '<p class="results__found">' + results.length + ' Result(s) found</p>'
        );

        function isResultAnOperation(result) {
            return (
                store[result.ref].tags.includes('bleOperation') ||
                store[result.ref].tags.includes('httpOperation')
            );
        }

        // Split into operation and other results(
        let operationResults = results.filter((result) => isResultAnOperation(result));
        let jekyllResults = results.filter((result) => !isResultAnOperation(result));

        function displayResults(results) {
            results.forEach((result) => {
                let ref = result.ref;
                let excerpt = store[ref].excerpt;
                let searchitem =
                    '<div class="list__item">' +
                    '<article class="archive__item" itemscope itemtype="https://schema.org/CreativeWork">' +
                    '<h2 class="archive__item-title" itemprop="headline">' +
                    '<a href="' +
                    store[ref].url +
                    '" rel="permalink">' +
                    store[ref].title +
                    '</a>' +
                    '</h2>';

                // For each match in this result...
                for (const metadata of Object.values(result.matchData.metadata)) {
                    // TODO what is going on here? It's not working for some results, presumably titles.
                    if (metadata.excerpt) {
                        for (position_item in metadata.excerpt['position']) {
                            let position = metadata.excerpt['position'][position_item];
                            let match_start = position[0];
                            let match_end = match_start + position[1];
                            let snippet_start = Math.max(
                                0,
                                match_start - SNIPPET_LEN / 2
                            );
                            let snippet_end = Math.min(
                                match_end - match_start + snippet_start + SNIPPET_LEN,
                                excerpt.length
                            );
                            searchitem +=
                                '<p class="archive__item-excerpt" itemprop="description">...' +
                                excerpt.slice(snippet_start, match_start) +
                                '<mark>' +
                                excerpt.slice(match_start, match_end) +
                                '</mark>' +
                                excerpt.slice(match_end, snippet_end) +
                                '...</p><br>';
                        }
                    }
                };
                searchitem += '</article></div>';
                resultdiv.append(searchitem);
            });
        }

        displayResults(operationResults);
        displayResults(jekyllResults);
    });
});
