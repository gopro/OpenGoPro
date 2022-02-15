// Build the store
var idx = lunr(function () {
    this.field('title');
    this.field('excerpt');
    this.field('categories'); // Not currently used
    this.field('tags'); // Not currently used
    this.ref('id');
    this.metadataWhitelist = ['position'];

    for (var item in store) {
        this.add({
            title: store[item].title,
            excerpt: store[item].excerpt,
            categories: store[item].categories,
            tags: store[item].tags,
            id: item,
        });
    }
});

const SNIPPET_LEN = 200;

$(document).ready(function () {
    $('input#search').on('keyup', function () {
        // Build and perform the search
        var resultdiv = $('#results');
        var query = $(this).val().toLowerCase();
        var results = idx.query(function (q) {
            // Now add terms for individual words
            query.split(lunr.tokenizer.separator).forEach(function (term) {
                // Actual search term with no wildcards get a big boost
                q.term(term, { fields: ['excerpt'], boost: 100 });
                // Term with wildcards gets a smaller boost
                if (query.lastIndexOf(' ') != query.length - 1) {
                    q.term(term, {
                        fields: ['excerpt'],
                        wildcard: lunr.Query.wildcard.TRAILING,
                        boost: 10,
                    });
                }
                // Add fuzziness of 1 character change with no boost
                if (term != '') {
                    q.term(term, { fields: ['excerpt'], editDistance: 1 });
                }
            });
        });
        // Build and display the results
        resultdiv.empty();
        resultdiv.prepend(
            '<p class="results__found">' + results.length + ' Result(s) found</p>'
        );
        for (var item in results) {
            var ref = results[item].ref;
            var excerpt = store[ref].excerpt;
            var searchitem =
                '<div class="list__item">' +
                '<article class="archive__item" itemscope itemtype="https://schema.org/CreativeWork">' +
                '<h2 class="archive__item-title" itemprop="headline">' +
                '<a href="' +
                store[ref].url +
                '" rel="permalink">' +
                store[ref].title +
                '</a>' +
                '</h2>';
            for (metadata_item in results[item].matchData.metadata) {
                var metadata = results[item].matchData.metadata[metadata_item];
                for (position_item in metadata.excerpt['position']) {
                    var position = metadata.excerpt['position'][position_item];
                    var match_start = position[0];
                    var match_end = match_start + position[1];
                    var snippet_start = Math.max(0, match_start - SNIPPET_LEN / 2);
                    var snippet_end = Math.min(
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
            searchitem += '</article></div>';
            resultdiv.append(searchitem);
        }
    });
});
