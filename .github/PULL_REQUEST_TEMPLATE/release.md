# Release Pull Request

## Version
<!-- Specify the new version number (e.g., 1.4.0) -->

## Release Date
<!-- Proposed date for this release -->

## Release Type
- [ ] Major (breaking changes)
- [ ] Minor (new features, non-breaking)
- [ ] Patch (bug fixes, non-breaking)

## Change Summary
<!-- Provide a high-level summary of the changes in this release -->

## Key Changes
<!-- List the major changes/features included in this release -->

## Breaking Changes
<!-- If applicable, list all breaking changes and migration instructions -->

## Dependencies
<!-- List any new or updated dependencies -->

## Deprecations 
- While `get_element_text()` is still supported, it is **recommended** to use the new async property `element.text`.


## Documentation
<!-- Link to updated documentation -->

## Release Checklist
- [ ] Version number updated in pyproject.toml
- [ ] Version number updated in cz.yaml
- [ ] CHANGELOG.md updated with all changes
- [ ] All tests passing
- [ ] Documentation updated
- [ ] API reference updated
- [ ] Breaking changes documented
- [ ] Migration guides prepared (if applicable)

## Additional Release Notes
<!-- Any additional information that should be included in release notes --> 