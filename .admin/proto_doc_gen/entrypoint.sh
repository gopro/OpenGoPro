#!/usr/bin/env bash

function build_proto_docs() {
    pushd /protos >/dev/null
    protoc --doc_out=/site --doc_opt=/site/_layouts/protobuf_markdown.tmpl,protos.md ./*.proto
    popd >/dev/null
}

echo "📇 Building protobuf docs..."
build_proto_docs

function watch_proto_docs() {
    echo "Watching for protobuf changes..."
    fswatch -m poll_monitor /protos/* |
        while read event; do
            echo "fswatch: $event modified"
            echo "fswatch: 📇 Rebuilding protobuf docs ..."
            build_proto_docs
            touch /site/protos.md
            echo "fswatch: Done"
        done
}

if [[ -z "$@" ]]; then
    watch_proto_docs
else
    watch_proto_docs &
    echo "Running $@"
    exec "$@"
fi
