d3.json('tasks', function(json) {
  var modules = d3.select('#modules')
      .selectAll('li')
      .data(json)
    .enter()
      .append('li')
      .attr('class', 'module')

  modules
    .append('h2')
      .text(function(d) {
        return d.module
      })

  var tasks = modules
    .append('ul')
      .selectAll('li')
      .data(function(d) {
        return d.tasks.map(function(task) {
          task.module = d.module
          return task
        })
      })
      .enter()
    .append('li')
      .attr('class', 'task')
    .append('a')
      .attr('href', 'javascript:void(0)')
      .text(function(d) {
        return d.class
      })
      .on('click', function(d) {
        var data = {
          module: d.module,
          class: d.class
        }

        var url = 'tasks'

        d3.xhr(url)
          .header('Content-Type', 'application/json')
          .post(JSON.stringify(data), function(err, req) {
            if (err) {
              console.error(err)
            } else {
              try {
                console.log(JSON.parse(req.response))
              } catch (err) {
                console.error('Could not parse response JSON', err)
              }
            }

          })
      })
})
